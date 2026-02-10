"""
Gemini AI Service - Tối ưu chi phí với Gemini 1.5 Flash.
Xử lý tất cả tương tác với Google Generative AI.
"""
import google.generativeai as genai
from google.generativeai.types import GenerationConfig
import time
import asyncio
from typing import Optional, Dict, Any
from functools import lru_cache

from app.config import get_settings

settings = get_settings()


class GeminiService:
    """
    Service quản lý kết nối và gọi Gemini API.
    Tối ưu: Sử dụng Flash cho hầu hết tác vụ, Flash-8B cho tác vụ đơn giản.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Khởi tạo với API key.
        Hỗ trợ BYOK (Bring Your Own Key) cho enterprise.
        """
        self.api_key = api_key or settings.GEMINI_API_KEY
        genai.configure(api_key=self.api_key)
        
        # Model instances - cached
        self._model_flash = None
        self._model_flash_8b = None
    
    @property
    def model_flash(self):
        """Gemini 1.5 Flash - Model chính cho KHBD."""
        if self._model_flash is None:
            self._model_flash = genai.GenerativeModel(
                model_name=settings.GEMINI_MODEL,
                generation_config=GenerationConfig(
                    temperature=settings.AI_TEMPERATURE,
                    max_output_tokens=settings.AI_MAX_OUTPUT_TOKENS,
                    top_p=0.95,
                    top_k=40,
                )
            )
        return self._model_flash
    
    @property
    def model_flash_8b(self):
        """Gemini 1.5 Flash-8B - Cho tác vụ đơn giản (tiết kiệm 50%)."""
        if self._model_flash_8b is None:
            self._model_flash_8b = genai.GenerativeModel(
                model_name=settings.GEMINI_MODEL_SIMPLE,
                generation_config=GenerationConfig(
                    temperature=0.5,
                    max_output_tokens=4096,
                )
            )
        return self._model_flash_8b
    
    async def generate_content(
        self,
        prompt: str,
        system_instruction: str = "",
        use_simple_model: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Tạo nội dung từ Gemini API.
        
        Args:
            prompt: Nội dung prompt chính
            system_instruction: Chỉ thị hệ thống (role)
            use_simple_model: Dùng Flash-8B thay vì Flash
            temperature: Override temperature nếu cần
            max_tokens: Override max_output_tokens nếu cần
            
        Returns:
            {
                "content": str,           # Nội dung sinh ra
                "tokens_input": int,      # Số token input
                "tokens_output": int,     # Số token output
                "generation_time_ms": int # Thời gian xử lý
            }
        """
        start_time = time.time()
        
        # Chọn model
        model = self.model_flash_8b if use_simple_model else self.model_flash
        
        # Build full prompt với system instruction
        full_prompt = prompt
        if system_instruction:
            full_prompt = f"{system_instruction}\n\n---\n\n{prompt}"
        
        # Override generation config nếu cần
        gen_config = None
        if temperature is not None or max_tokens is not None:
            gen_config = GenerationConfig(
                temperature=temperature if temperature is not None else settings.AI_TEMPERATURE,
                max_output_tokens=max_tokens if max_tokens is not None else settings.AI_MAX_OUTPUT_TOKENS,
            )
        
        try:
            # Gọi API async
            response = await asyncio.to_thread(
                model.generate_content,
                full_prompt,
                generation_config=gen_config,
            )
            
            generation_time_ms = int((time.time() - start_time) * 1000)
            
            # Extract usage metadata
            usage_metadata = response.usage_metadata if hasattr(response, 'usage_metadata') else None
            tokens_input = usage_metadata.prompt_token_count if usage_metadata else 0
            tokens_output = usage_metadata.candidates_token_count if usage_metadata else 0
            
            return {
                "content": response.text,
                "tokens_input": tokens_input,
                "tokens_output": tokens_output,
                "generation_time_ms": generation_time_ms,
            }
            
        except Exception as e:
            raise GeminiError(f"Lỗi khi gọi Gemini API: {str(e)}")
    
    async def generate_khbd(
        self,
        subject: str,
        grade: int,
        lesson_name: str,
        duration: int,
        system_prompt: str,
        additional_context: str = "",
    ) -> Dict[str, Any]:
        """
        Tạo Kế hoạch bài dạy (KHBD).
        
        Args:
            subject: Môn học (khtn, nguvan, ...)
            grade: Lớp (6-9)
            lesson_name: Tên bài học
            duration: Số tiết
            system_prompt: System instruction đã được chuẩn bị
            additional_context: Context bổ sung (PPCT, đặc điểm trường...)
        """
        user_prompt = f"""
Hãy soạn Kế hoạch bài dạy chi tiết với thông tin sau:

**Môn học:** {subject}
**Lớp:** {grade}
**Tên bài:** {lesson_name}
**Thời lượng:** {duration} tiết

{additional_context}
"""
        
        return await self.generate_content(
            prompt=user_prompt,
            system_instruction=system_prompt,
            use_simple_model=False,  # KHBD cần model tốt
        )
    
    async def generate_skkn_ideation(
        self,
        subject: str,
        grade: int,
        problem: str,
        school_context: str = "",
    ) -> Dict[str, Any]:
        """
        SKKN Bước 1: Đề xuất 5 đề tài sáng kiến.
        Dùng Flash-8B vì tác vụ đơn giản.
        """
        system_prompt = """Bạn là chuyên gia tư vấn sáng kiến kinh nghiệm giáo dục.
Nhiệm vụ: Đề xuất 5 đề tài SKKN có tính mới, thực tiễn, khả thi.

Định dạng output (Markdown):
## Đề tài 1: [Tên đề tài]
**Tính cấp thiết:** [Phân tích ngắn gọn]
**Điểm mới:** [Điều gì khác biệt so với SKKN thông thường]
**Độ khả thi:** [Cao/Trung bình/Thấp] - [Giải thích]

(Lặp lại cho 5 đề tài)

## Khuyến nghị
[Đề xuất đề tài phù hợp nhất và lý do]"""

        user_prompt = f"""
**Môn học:** {subject}
**Khối lớp:** {grade}
**Vấn đề cần giải quyết:** {problem}
**Bối cảnh trường học:** {school_context or "Trường THCS thông thường"}

Hãy đề xuất 5 đề tài SKKN phù hợp.
"""
        
        return await self.generate_content(
            prompt=user_prompt,
            system_instruction=system_prompt,
            use_simple_model=True,  # Dùng 8B cho tiết kiệm
            temperature=0.8,  # Tăng creativity
        )
    
    async def generate_skkn_outline(
        self,
        topic: str,
        subject: str,
        school_context: str = "",
    ) -> Dict[str, Any]:
        """
        SKKN Bước 2: Lập dàn ý chi tiết 3 cấp.
        """
        system_prompt = """Bạn là chuyên gia soạn thảo sáng kiến kinh nghiệm.
Nhiệm vụ: Lập dàn ý chi tiết 3 cấp (I, 1, a) cho SKKN.

Cấu trúc BẮT BUỘC:
# [TÊN ĐỀ TÀI]

## PHẦN I: MỞ ĐẦU
### 1. Lý do chọn đề tài
### 2. Mục đích nghiên cứu
### 3. Đối tượng và phạm vi
### 4. Phương pháp nghiên cứu

## PHẦN II: NỘI DUNG
### 1. Cơ sở lý luận
### 2. Thực trạng vấn đề
#### 2.1. Thuận lợi
#### 2.2. Khó khăn
#### 2.3. Số liệu khảo sát ban đầu
### 3. Các biện pháp thực hiện
#### 3.1. Biện pháp 1: [Tên]
#### 3.2. Biện pháp 2: [Tên]
#### 3.3. Biện pháp 3: [Tên]
### 4. Hiệu quả của sáng kiến
#### 4.1. Kết quả định lượng
#### 4.2. Kết quả định tính

## PHẦN III: KẾT LUẬN VÀ KIẾN NGHỊ
### 1. Kết luận
### 2. Kiến nghị

## TÀI LIỆU THAM KHẢO"""

        user_prompt = f"""
**Đề tài:** {topic}
**Môn học:** {subject}
**Bối cảnh:** {school_context or "Trường THCS"}

Hãy lập dàn ý chi tiết. Đặt tên cụ thể cho các biện pháp phù hợp với đề tài.
"""
        
        return await self.generate_content(
            prompt=user_prompt,
            system_instruction=system_prompt,
            use_simple_model=False,
        )
    
    async def generate_skkn_section(
        self,
        topic: str,
        outline: str,
        section_title: str,
        previous_content: str = "",
        school_context: str = "",
    ) -> Dict[str, Any]:
        """
        SKKN Bước 3: Viết nội dung từng phần.
        """
        system_prompt = f"""Bạn là nhà giáo có kinh nghiệm viết sáng kiến kinh nghiệm.
Nhiệm vụ: Viết chi tiết phần "{section_title}" của SKKN.

Yêu cầu:
- Văn phong trang trọng, khoa học
- Đưa ví dụ cụ thể, thực tế
- Độ dài: 800-1200 từ cho mỗi phần
- Sử dụng Markdown cho format
- Nếu có công thức: dùng LaTeX ($...$)
- Nếu là bảng số liệu: dùng Markdown Table

Bối cảnh để cá nhân hóa: {school_context or "Trường THCS thông thường"}
"""

        user_prompt = f"""
**Đề tài:** {topic}

**Dàn ý tổng thể:**
{outline}

**Phần cần viết:** {section_title}

**Nội dung đã viết trước đó (để đảm bảo liên kết):**
{previous_content[:2000] if previous_content else "Đây là phần đầu tiên."}

Hãy viết chi tiết phần này.
"""
        
        return await self.generate_content(
            prompt=user_prompt,
            system_instruction=system_prompt,
            use_simple_model=False,
            temperature=0.75,  # Tăng creativity
        )
    
    def estimate_cost(self, tokens_input: int, tokens_output: int, model: str = "flash") -> float:
        """
        Ước tính chi phí USD.
        
        Pricing (per 1M tokens):
        - Flash: Input $0.075, Output $0.30
        - Flash-8B: Input $0.0375, Output $0.15
        """
        if model == "flash":
            input_cost = (tokens_input / 1_000_000) * 0.075
            output_cost = (tokens_output / 1_000_000) * 0.30
        else:  # flash-8b
            input_cost = (tokens_input / 1_000_000) * 0.0375
            output_cost = (tokens_output / 1_000_000) * 0.15
        
        return input_cost + output_cost


class GeminiError(Exception):
    """Custom exception for Gemini API errors."""
    pass


# Singleton instance
@lru_cache()
def get_gemini_service(api_key: Optional[str] = None) -> GeminiService:
    """Get cached GeminiService instance."""
    return GeminiService(api_key)
