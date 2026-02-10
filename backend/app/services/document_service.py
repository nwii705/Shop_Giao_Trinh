"""
Document Service - Chuyển đổi Markdown sang Word (.docx)
Sử dụng python-docx trực tiếp, không cần Pandoc
"""

import os
import re
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Tuple
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


class DocumentConverter:
    """
    Chuyển đổi Markdown sang Word không cần Pandoc.
    Hỗ trợ bảng, heading, bold/italic, LaTeX formulas.
    """
    
    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    async def convert_markdown_to_docx(
        self,
        markdown_content: str,
        output_filename: str,
    ) -> str:
        """
        Chuyển đổi Markdown thành Word.
        
        Args:
            markdown_content: Nội dung Markdown có thể chứa LaTeX
            output_filename: Tên file đầu ra (không cần .docx)
            
        Returns:
            Đường dẫn đến file .docx đã tạo
        """
        # Chạy conversion trong thread riêng để không block
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, 
            self._convert_sync, 
            markdown_content, 
            output_filename
        )
    
    def _convert_sync(self, markdown_content: str, output_filename: str) -> str:
        """Phiên bản sync của conversion."""
        doc = Document()
        
        # Thiết lập style
        self._setup_styles(doc)
        
        # Parse và render markdown
        self._parse_markdown(doc, markdown_content)
        
        # Tạo tên file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = self._sanitize_filename(output_filename)
        output_path = self.output_dir / f"{safe_filename}_{timestamp}.docx"
        
        # Lưu file
        doc.save(str(output_path))
        return str(output_path)
    
    def _setup_styles(self, doc: Document):
        """Thiết lập các style mặc định cho document."""
        styles = doc.styles
        
        # Style cho Normal text
        normal = styles['Normal']
        normal.font.name = 'Times New Roman'
        normal.font.size = Pt(13)
        normal._element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')
        
        # Style cho Heading 1
        if 'Heading 1' in styles:
            h1 = styles['Heading 1']
            h1.font.name = 'Times New Roman'
            h1.font.size = Pt(14)
            h1.font.bold = True
            h1.font.color.rgb = RGBColor(0, 0, 0)
        
        # Style cho Heading 2
        if 'Heading 2' in styles:
            h2 = styles['Heading 2']
            h2.font.name = 'Times New Roman'
            h2.font.size = Pt(13)
            h2.font.bold = True
            h2.font.color.rgb = RGBColor(0, 0, 0)
        
        # Style cho Heading 3
        if 'Heading 3' in styles:
            h3 = styles['Heading 3']
            h3.font.name = 'Times New Roman'
            h3.font.size = Pt(13)
            h3.font.bold = True
            h3.font.italic = True
            h3.font.color.rgb = RGBColor(0, 0, 0)
    
    def _parse_markdown(self, doc: Document, content: str):
        """Parse markdown và thêm vào document."""
        lines = content.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Skip empty lines
            if not line.strip():
                i += 1
                continue
            
            # Heading
            if line.startswith('#'):
                self._add_heading(doc, line)
                i += 1
                continue
            
            # Table (bắt đầu bằng |)
            if line.strip().startswith('|'):
                table_lines = []
                while i < len(lines) and lines[i].strip().startswith('|'):
                    table_lines.append(lines[i])
                    i += 1
                self._add_table(doc, table_lines)
                continue
            
            # Bullet list
            if line.strip().startswith('- ') or line.strip().startswith('* '):
                self._add_list_item(doc, line)
                i += 1
                continue
            
            # Numbered list
            if re.match(r'^\s*\d+\.\s', line):
                self._add_numbered_item(doc, line)
                i += 1
                continue
            
            # Normal paragraph
            self._add_paragraph(doc, line)
            i += 1
    
    def _add_heading(self, doc: Document, line: str):
        """Thêm heading vào document."""
        # Đếm số #
        match = re.match(r'^(#+)\s*(.+)$', line)
        if match:
            level = min(len(match.group(1)), 3)  # Max level 3
            text = match.group(2)
            
            # Xử lý inline formatting trong heading
            p = doc.add_heading('', level=level)
            self._add_formatted_text(p, text)
    
    def _add_paragraph(self, doc: Document, line: str):
        """Thêm paragraph với formatting."""
        p = doc.add_paragraph()
        self._add_formatted_text(p, line)
    
    def _add_list_item(self, doc: Document, line: str):
        """Thêm bullet list item."""
        text = re.sub(r'^\s*[-*]\s*', '', line)
        p = doc.add_paragraph(style='List Bullet')
        self._add_formatted_text(p, text)
    
    def _add_numbered_item(self, doc: Document, line: str):
        """Thêm numbered list item."""
        text = re.sub(r'^\s*\d+\.\s*', '', line)
        p = doc.add_paragraph(style='List Number')
        self._add_formatted_text(p, text)
    
    def _add_formatted_text(self, paragraph, text: str):
        """
        Thêm text với formatting (bold, italic, LaTeX).
        Chuyển LaTeX thành text với ký hiệu Unicode.
        """
        # Pattern để tìm các phần cần format
        # LaTeX inline: $...$
        # Bold: **...**
        # Italic: *...*
        # Bold-Italic: ***...***
        # Code: `...`
        
        pattern = r'(\*\*\*[^*]+\*\*\*|\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`|\$[^$]+\$|<br>)'
        parts = re.split(pattern, text)
        
        for part in parts:
            if not part:
                continue
            
            # Bold + Italic
            if part.startswith('***') and part.endswith('***'):
                run = paragraph.add_run(part[3:-3])
                run.bold = True
                run.italic = True
            # Bold
            elif part.startswith('**') and part.endswith('**'):
                run = paragraph.add_run(part[2:-2])
                run.bold = True
            # Italic
            elif part.startswith('*') and part.endswith('*') and len(part) > 2:
                run = paragraph.add_run(part[1:-1])
                run.italic = True
            # Code
            elif part.startswith('`') and part.endswith('`'):
                run = paragraph.add_run(part[1:-1])
                run.font.name = 'Courier New'
                run.font.size = Pt(11)
            # LaTeX formula
            elif part.startswith('$') and part.endswith('$'):
                latex = part[1:-1]
                converted = self._latex_to_unicode(latex)
                run = paragraph.add_run(converted)
                run.italic = True
            # Line break
            elif part == '<br>':
                paragraph.add_run().add_break()
            else:
                paragraph.add_run(part)
    
    def _latex_to_unicode(self, latex: str) -> str:
        """
        Chuyển LaTeX đơn giản thành Unicode text.
        Hỗ trợ các công thức phổ biến trong KHTN.
        """
        text = latex
        
        # Subscript numbers: _2 -> ₂
        subscript_map = {
            '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
            '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉',
            'a': 'ₐ', 'e': 'ₑ', 'h': 'ₕ', 'i': 'ᵢ', 'j': 'ⱼ',
            'k': 'ₖ', 'l': 'ₗ', 'm': 'ₘ', 'n': 'ₙ', 'o': 'ₒ',
            'p': 'ₚ', 'r': 'ᵣ', 's': 'ₛ', 't': 'ₜ', 'u': 'ᵤ',
            'v': 'ᵥ', 'x': 'ₓ',
        }
        
        # Superscript: ^2 -> ²
        superscript_map = {
            '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
            '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
            '+': '⁺', '-': '⁻', '=': '⁼', '(': '⁽', ')': '⁾',
            'n': 'ⁿ', 'i': 'ⁱ', 'o': '°',
        }
        
        # Greek letters
        greek_map = {
            r'\alpha': 'α', r'\beta': 'β', r'\gamma': 'γ', r'\delta': 'δ',
            r'\epsilon': 'ε', r'\zeta': 'ζ', r'\eta': 'η', r'\theta': 'θ',
            r'\iota': 'ι', r'\kappa': 'κ', r'\lambda': 'λ', r'\mu': 'μ',
            r'\nu': 'ν', r'\xi': 'ξ', r'\pi': 'π', r'\rho': 'ρ',
            r'\sigma': 'σ', r'\tau': 'τ', r'\phi': 'φ', r'\chi': 'χ',
            r'\psi': 'ψ', r'\omega': 'ω',
            r'\Alpha': 'Α', r'\Beta': 'Β', r'\Gamma': 'Γ', r'\Delta': 'Δ',
            r'\Omega': 'Ω', r'\Sigma': 'Σ', r'\Pi': 'Π',
        }
        
        # Math symbols
        symbol_map = {
            r'\times': '×', r'\div': '÷', r'\pm': '±', r'\mp': '∓',
            r'\cdot': '·', r'\bullet': '•',
            r'\leq': '≤', r'\geq': '≥', r'\neq': '≠', r'\approx': '≈',
            r'\equiv': '≡', r'\propto': '∝',
            r'\infty': '∞', r'\partial': '∂', r'\nabla': '∇',
            r'\sum': 'Σ', r'\prod': 'Π', r'\int': '∫',
            r'\sqrt': '√', r'\cbrt': '∛',
            r'\rightarrow': '→', r'\leftarrow': '←', r'\Rightarrow': '⇒',
            r'\xrightarrow': '→',
            r'\degree': '°', r'\circ': '°',
            r'\angle': '∠', r'\triangle': '△', r'\square': '□',
            r'\frac': '',  # Xử lý riêng
        }
        
        # Replace Greek letters
        for latex_cmd, unicode_char in greek_map.items():
            text = text.replace(latex_cmd, unicode_char)
        
        # Replace symbols
        for latex_cmd, unicode_char in symbol_map.items():
            text = text.replace(latex_cmd, unicode_char)
        
        # Handle fractions: \frac{a}{b} -> a/b
        frac_pattern = r'\\frac\{([^}]+)\}\{([^}]+)\}'
        text = re.sub(frac_pattern, r'\1/\2', text)
        
        # Handle xrightarrow with label: \xrightarrow{t^o} -> →(t°)
        xarrow_pattern = r'\\xrightarrow\{([^}]+)\}'
        text = re.sub(xarrow_pattern, r' →[\1] ', text)
        
        # Handle subscripts: _{...} or _x
        def replace_subscript(match):
            content = match.group(1) if match.group(1) else match.group(2)
            result = ''
            for char in content:
                mapped = subscript_map.get(char)
                result += mapped if mapped else char
            return result
        
        text = re.sub(r'_\{([^}]+)\}|_([a-zA-Z0-9])', replace_subscript, text)
        
        # Handle superscripts: ^{...} or ^x
        def replace_superscript(match):
            content = match.group(1) if match.group(1) else match.group(2)
            result = ''
            for char in content:
                mapped = superscript_map.get(char)
                result += mapped if mapped else char
            return result
        
        text = re.sub(r'\^\{([^}]+)\}|\^([a-zA-Z0-9+\-])', replace_superscript, text)
        
        # Clean up remaining LaTeX commands
        text = re.sub(r'\\[a-zA-Z]+', '', text)
        text = re.sub(r'[{}]', '', text)
        text = text.strip()
        
        return text
    
    def _add_table(self, doc: Document, table_lines: List[str]):
        """Parse và thêm bảng từ markdown."""
        if len(table_lines) < 2:
            return
        
        # Parse header
        header = self._parse_table_row(table_lines[0])
        if not header:
            return
        
        # Skip separator line (|---|---|)
        data_start = 1
        if len(table_lines) > 1 and re.match(r'^\|[-:\s|]+\|$', table_lines[1].strip()):
            data_start = 2
        
        # Parse data rows
        rows = []
        for i in range(data_start, len(table_lines)):
            row = self._parse_table_row(table_lines[i])
            if row:
                rows.append(row)
        
        # Tạo table
        num_cols = len(header)
        table = doc.add_table(rows=1 + len(rows), cols=num_cols)
        table.style = 'Table Grid'
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        # Header row
        header_cells = table.rows[0].cells
        for i, cell_text in enumerate(header):
            if i < num_cols:
                p = header_cells[i].paragraphs[0]
                self._add_formatted_text(p, cell_text.strip())
                # Bold header
                for run in p.runs:
                    run.bold = True
        
        # Data rows
        for row_idx, row_data in enumerate(rows):
            cells = table.rows[row_idx + 1].cells
            for col_idx, cell_text in enumerate(row_data):
                if col_idx < num_cols:
                    p = cells[col_idx].paragraphs[0]
                    self._add_formatted_text(p, cell_text.strip())
        
        # Set column widths (auto-fit)
        for col in table.columns:
            for cell in col.cells:
                cell.width = Cm(8)
        
        # Add spacing after table
        doc.add_paragraph()
    
    def _parse_table_row(self, line: str) -> List[str]:
        """Parse một dòng table markdown."""
        line = line.strip()
        if not line.startswith('|') or not line.endswith('|'):
            return []
        
        # Split by | và bỏ cells rỗng đầu/cuối
        cells = line.split('|')[1:-1]
        return [cell.strip() for cell in cells]
    
    def _sanitize_filename(self, filename: str) -> str:
        """Loại bỏ ký tự không hợp lệ khỏi tên file."""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename[:100]


class ConversionError(Exception):
    """Exception khi chuyển đổi thất bại."""
    pass


# ============== QUICK CONVERT FUNCTIONS ==============

async def quick_convert(
    markdown: str,
    filename: str = "document",
) -> str:
    """
    Hàm tiện ích để convert nhanh.
    
    Usage:
        path = await quick_convert(markdown_content, "giao_an_bai_1")
    """
    converter = DocumentConverter()
    return await converter.convert_markdown_to_docx(markdown, filename)


def convert_sync(
    markdown: str,
    filename: str = "document",
) -> str:
    """
    Phiên bản sync cho testing.
    """
    converter = DocumentConverter()
    return converter._convert_sync(markdown, filename)


# ============== EXAMPLE USAGE ==============

EXAMPLE_MARKDOWN = """
# BÀI 2: OXYGEN

## I. MỤC TIÊU

### 1. Kiến thức
- Nêu được tính chất vật lý của oxygen $O_2$
- Viết được phương trình phản ứng: $2Mg + O_2 \\xrightarrow{t^o} 2MgO$
- Tính khối lượng riêng: $\\rho = \\frac{m}{V}$

### 2. Năng lực
- Nhận thức khoa học tự nhiên
- Tìm hiểu tự nhiên

## II. THIẾT BỊ DẠY HỌC

| Giáo viên | Học sinh |
|-----------|----------|
| SGK, SGV | SGK, vở ghi |
| Bình oxygen | Que đóm |

## III. TIẾN TRÌNH DẠY HỌC

### A. HOẠT ĐỘNG KHỞI ĐỘNG

| Hoạt động của GV và HS | Sản phẩm dự kiến |
|------------------------|------------------|
| **Bước 1: Chuyển giao nhiệm vụ**<br>GV: Các em hãy kể tên các khí có trong không khí | |
| **Bước 2: Thực hiện nhiệm vụ**<br>HS: Thảo luận nhóm 2 phút | HS liệt kê: $O_2$, $N_2$, $CO_2$... |
| **Bước 3: Báo cáo**<br>Đại diện nhóm trình bày | |
| **Bước 4: Kết luận**<br>GV: Chốt kiến thức về thành phần không khí | Oxygen chiếm 21% không khí |
"""


if __name__ == "__main__":
    # Test conversion
    output = convert_sync(EXAMPLE_MARKDOWN, "test_giao_an")
    print(f"File created: {output}")
