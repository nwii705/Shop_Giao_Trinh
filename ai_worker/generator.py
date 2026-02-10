"""
EduShop AI Worker - Tự động tạo giáo trình bằng AI
Sử dụng Gemini API (xoay vòng 5 keys) và FPDF để xuất PDF
"""

import sys
import os
import io

# Fix encoding cho Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import random
import time
from datetime import datetime
from dotenv import load_dotenv

# Load biến môi trường
load_dotenv()

import pymongo
import google.generativeai as genai
from fpdf import FPDF

# --- CẤU HÌNH ---
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/EduShopDB')

# Load tất cả API keys và xoay vòng (6 keys)
GEMINI_API_KEYS = [
    os.getenv('GEMINI_API_KEY_1', ''),
    os.getenv('GEMINI_API_KEY_2', ''),
    os.getenv('GEMINI_API_KEY_3', ''),
    os.getenv('GEMINI_API_KEY_4', ''),
    os.getenv('GEMINI_API_KEY_5', ''),
    os.getenv('GEMINI_API_KEY_6', ''),
]
# Lọc bỏ key rỗng
GEMINI_API_KEYS = [k for k in GEMINI_API_KEYS if k]

# Biến theo dõi key đang dùng
current_key_index = 0

# Category mapping
CATEGORY_MAP = {
    'ai': {
        'name': 'AI & Công nghệ số',
        'icon': '🤖',
        'keywords': ['AI', 'trí tuệ nhân tạo', 'công nghệ số', 'Gemini', 'ChatGPT', 'phần mềm', 'Azota', 'Phyphox']
    },
    'stem': {
        'name': 'STEM & Dự án',
        'icon': '🔬',
        'keywords': ['STEM', 'dự án', 'thực hành', 'khám phá', 'sáng tạo', 'nhà khoa học nhỏ']
    },
    'method': {
        'name': 'Phương pháp dạy học',
        'icon': '📝',
        'keywords': ['phương pháp', 'dạy học', 'tư duy', 'năng lực', 'kỹ thuật', 'sơ đồ tư duy', 'dạy học trạm']
    },
    'skill': {
        'name': 'Kỹ năng & Thí nghiệm',
        'icon': '🧪',
        'keywords': ['kỹ năng sống', 'thí nghiệm', 'thực hành', 'tư duy khoa học', 'giáo dục toàn diện']
    }
}


def get_next_api_key():
    """Lấy API key tiếp theo theo vòng tròn"""
    global current_key_index
    
    if not GEMINI_API_KEYS:
        print("❌ Không có API key nào được cấu hình!")
        return None
    
    key = GEMINI_API_KEYS[current_key_index]
    print(f"🔑 Sử dụng API Key #{current_key_index + 1}/{len(GEMINI_API_KEYS)}")
    current_key_index = (current_key_index + 1) % len(GEMINI_API_KEYS)
    
    return key


def configure_gemini_with_rotation():
    """Cấu hình Gemini với key xoay vòng"""
    api_key = get_next_api_key()
    if not api_key:
        return None
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')


def try_generate_with_retry(prompt, max_retries=5):
    """Thử generate với nhiều API keys nếu bị rate limit"""
    for attempt in range(max_retries):
        try:
            model = configure_gemini_with_rotation()
            if not model:
                return None
            
            response = model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            error_str = str(e).lower()
            
            if 'quota' in error_str or 'rate' in error_str or 'limit' in error_str or '429' in error_str:
                print(f"   ⚠️ Key bị rate limit, thử key tiếp theo... (lần {attempt + 1}/{max_retries})")
                time.sleep(1)
                continue
            elif 'safety' in error_str or 'block' in error_str:
                print(f"   ⚠️ Nội dung bị chặn, thử lại với prompt khác...")
                time.sleep(0.5)
                continue
            else:
                print(f"   ❌ Lỗi: {e}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                return None
    
    print("   ❌ Đã thử hết tất cả API keys!")
    return None


def remove_vietnamese_accents(text):
    """Chuyển tiếng Việt có dấu thành không dấu cho PDF cơ bản"""
    accents = {
        'à': 'a', 'á': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a',
        'ă': 'a', 'ằ': 'a', 'ắ': 'a', 'ẳ': 'a', 'ẵ': 'a', 'ặ': 'a',
        'â': 'a', 'ầ': 'a', 'ấ': 'a', 'ẩ': 'a', 'ẫ': 'a', 'ậ': 'a',
        'è': 'e', 'é': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
        'ê': 'e', 'ề': 'e', 'ế': 'e', 'ể': 'e', 'ễ': 'e', 'ệ': 'e',
        'ì': 'i', 'í': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
        'ò': 'o', 'ó': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
        'ô': 'o', 'ồ': 'o', 'ố': 'o', 'ổ': 'o', 'ỗ': 'o', 'ộ': 'o',
        'ơ': 'o', 'ờ': 'o', 'ớ': 'o', 'ở': 'o', 'ỡ': 'o', 'ợ': 'o',
        'ù': 'u', 'ú': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
        'ư': 'u', 'ừ': 'u', 'ứ': 'u', 'ử': 'u', 'ữ': 'u', 'ự': 'u',
        'ỳ': 'y', 'ý': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y',
        'đ': 'd',
        'À': 'A', 'Á': 'A', 'Ả': 'A', 'Ã': 'A', 'Ạ': 'A',
        'Ă': 'A', 'Ằ': 'A', 'Ắ': 'A', 'Ẳ': 'A', 'Ẵ': 'A', 'Ặ': 'A',
        'Â': 'A', 'Ầ': 'A', 'Ấ': 'A', 'Ẩ': 'A', 'Ẫ': 'A', 'Ậ': 'A',
        'È': 'E', 'É': 'E', 'Ẻ': 'E', 'Ẽ': 'E', 'Ẹ': 'E',
        'Ê': 'E', 'Ề': 'E', 'Ế': 'E', 'Ể': 'E', 'Ễ': 'E', 'Ệ': 'E',
        'Ì': 'I', 'Í': 'I', 'Ỉ': 'I', 'Ĩ': 'I', 'Ị': 'I',
        'Ò': 'O', 'Ó': 'O', 'Ỏ': 'O', 'Õ': 'O', 'Ọ': 'O',
        'Ô': 'O', 'Ồ': 'O', 'Ố': 'O', 'Ổ': 'O', 'Ỗ': 'O', 'Ộ': 'O',
        'Ơ': 'O', 'Ờ': 'O', 'Ớ': 'O', 'Ở': 'O', 'Ỡ': 'O', 'Ợ': 'O',
        'Ù': 'U', 'Ú': 'U', 'Ủ': 'U', 'Ũ': 'U', 'Ụ': 'U',
        'Ư': 'U', 'Ừ': 'U', 'Ứ': 'U', 'Ử': 'U', 'Ữ': 'U', 'Ự': 'U',
        'Ỳ': 'Y', 'Ý': 'Y', 'Ỷ': 'Y', 'Ỹ': 'Y', 'Ỵ': 'Y',
        'Đ': 'D'
    }
    for viet, ascii_char in accents.items():
        text = text.replace(viet, ascii_char)
    return text


def connect_db():
    """Kết nối MongoDB"""
    try:
        client = pymongo.MongoClient(MONGO_URI)
        client.admin.command('ping')
        db = client["EduShopDB"]
        print("✅ Đã kết nối MongoDB Atlas")
        return db
    except Exception as e:
        print(f"❌ Lỗi kết nối MongoDB: {e}")
        sys.exit(1)


def create_content(category, quantity=1):
    """Tạo giáo trình mới bằng AI"""
    print(f"\n{'='*50}")
    print(f"🤖 AI Worker: Tạo {quantity} giáo trình [{category.upper()}]")
    print(f"{'='*50}")
    print(f"📌 Có {len(GEMINI_API_KEYS)} API keys để xoay vòng")
    
    db = connect_db()
    products_col = db["products"]
    
    cat_info = CATEGORY_MAP.get(category, CATEGORY_MAP['ai'])
    
    success_count = 0
    
    for i in range(int(quantity)):
        try:
            print(f"\n📝 [{i+1}/{quantity}] Đang tạo giáo trình...")
            
            # 1. Tạo tên đề tài
            prompt_title = f"""Viết 1 tên đề tài sáng kiến kinh nghiệm cho môn KHTN/Vật lí cấp THCS.
Lĩnh vực: {cat_info['name']}
Từ khóa: {', '.join(cat_info['keywords'][:3])}
Yêu cầu: Tiêu đề hấp dẫn 20-35 từ, đề cập lớp 6/7/8/9. CHỈ IN TIÊU ĐỀ."""
            
            title = try_generate_with_retry(prompt_title)
            if not title:
                print("   ❌ Không thể tạo tiêu đề")
                continue
            
            title = title.replace("*", "").replace('"', '').replace("**", "").strip()
            if title.startswith("Đề tài"):
                title = title.split(":", 1)[-1].strip()
            
            print(f"   📌 {title[:65]}...")
            
            # 2. Tạo nội dung
            prompt_body = f"""Viết tóm tắt 400 từ cho sáng kiến: "{title}"
Gồm: 1.ĐẶT VẤN ĐỀ 2.GIẢI PHÁP 3.KẾT QUẢ 4.KẾT LUẬN
Tiếng Việt, văn phong khoa học."""
            
            body = try_generate_with_retry(prompt_body)
            if not body:
                print("   ❌ Không thể tạo nội dung")
                continue
            
            # 3. Tạo PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, "SANG KIEN KINH NGHIEM", 0, 1, 'C')
            pdf.ln(5)
            
            pdf.set_font("Arial", 'I', 10)
            pdf.cell(0, 8, f"Linh vuc: {remove_vietnamese_accents(cat_info['name'])}", 0, 1, 'C')
            pdf.ln(5)
            
            pdf.set_font("Arial", 'B', 13)
            pdf.multi_cell(0, 8, f"DE TAI:\n{remove_vietnamese_accents(title)}")
            pdf.ln(8)
            
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(8)
            
            pdf.set_font("Arial", size=11)
            pdf.multi_cell(0, 6, remove_vietnamese_accents(body))
            
            pdf.ln(15)
            pdf.set_font("Arial", 'I', 9)
            pdf.set_text_color(128, 128, 128)
            pdf.cell(0, 8, f"EduShop - AI Generated - {datetime.now().strftime('%d/%m/%Y')}", 0, 1, 'C')
            
            timestamp = int(datetime.now().timestamp() * 1000)
            filename = f"giaotrinh_{category}_{timestamp}.pdf"
            docs_dir = os.path.join(os.path.dirname(__file__), '..', 'backend', 'public', 'docs')
            os.makedirs(docs_dir, exist_ok=True)
            pdf.output(os.path.join(docs_dir, filename))
            print(f"   📄 PDF: {filename}")
            
            # 4. Features
            features = ["AI Generated", "Mới 100%"]
            title_lower = title.lower()
            for grade in ['6', '7', '8', '9']:
                if f'khtn {grade}' in title_lower or f'lớp {grade}' in title_lower:
                    features.append(f"KHTN {grade}")
                    break
            else:
                features.append("THCS")
            features.append(random.choice(cat_info['keywords'][:4]))
            
            # 5. Lưu MongoDB
            base_price = random.randint(35, 55) * 10000
            
            new_product = {
                "title": title,
                "category": category,
                "categoryName": cat_info['name'],
                "categoryIcon": cat_info['icon'],
                "price": base_price,
                "originalPrice": int(base_price * 1.25),
                "features": features,
                "status": "available",
                "fileUrl": f"/docs/{filename}",
                "createdAt": datetime.now(),
                "generatedBy": "AI"
            }
            
            result = products_col.insert_one(new_product)
            print(f"   ✅ MongoDB ID: {result.inserted_id}")
            success_count += 1
            
            if i < int(quantity) - 1:
                time.sleep(2)
            
        except Exception as e:
            print(f"   ❌ Lỗi: {e}")
            continue
    
    print(f"\n{'='*50}")
    print(f"🎉 Hoàn thành: {success_count}/{quantity} giáo trình")
    print(f"{'='*50}\n")
    
    return success_count


if __name__ == "__main__":
    category = sys.argv[1] if len(sys.argv) > 1 else "ai"
    quantity = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    
    if category not in CATEGORY_MAP:
        print(f"⚠️ Category không hợp lệ: {', '.join(CATEGORY_MAP.keys())}")
        category = "ai"
    
    create_content(category, quantity)
