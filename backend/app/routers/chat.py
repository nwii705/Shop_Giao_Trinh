"""
Chat Router - API cho chatbot sử dụng Gemini AI.
Trả lời câu hỏi về giáo dục, giáo án, sách giáo khoa.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.database.models import User
from app.auth import get_current_user
from app.services.gemini_service import get_gemini_service
from app.config import get_settings

settings = get_settings()
router = APIRouter()


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []
    context: Optional[str] = None  # Thông tin bổ sung (môn học, lớp, etc.)


class ChatResponse(BaseModel):
    reply: str
    tokens_used: int = 0


# System prompt cho chatbot giáo dục
CHAT_SYSTEM_PROMPT = """Bạn là GiaoTrinh AI - trợ lý thông minh hỗ trợ giáo viên Việt Nam.

# VAI TRÒ
Bạn là chuyên gia giáo dục, am hiểu:
- Chương trình Giáo dục Phổ thông 2018
- Công văn 5512/BGDĐT-GDTrH về Kế hoạch bài dạy
- Các bộ sách: Chân trời sáng tạo, Kết nối tri thức, Cánh diều
- Phương pháp dạy học tích cực (5E, Jigsaw, KWL, etc.)

# NHIỆM VỤ
- Trả lời câu hỏi về giáo dục, giáo án, phương pháp giảng dạy
- Hướng dẫn soạn giáo án theo chuẩn Công văn 5512
- Giải thích kiến thức các môn KHTN, Ngữ văn, Toán, etc.
- Tư vấn về sách giáo khoa, tài liệu tham khảo

# PHONG CÁCH
- Thân thiện, chuyên nghiệp
- Trả lời bằng tiếng Việt
- Sử dụng Markdown để định dạng
- Công thức toán/hóa dùng LaTeX: $công_thức$

# LƯU Ý
- Nếu không chắc chắn, hãy nói rõ
- Khuyến khích GV tham khảo SGK chính thức
- Không tạo nội dung không phù hợp với giáo dục
"""


@router.post("/send", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Gửi tin nhắn và nhận phản hồi từ AI.
    """
    gemini = get_gemini_service()
    
    # Build conversation history
    conversation = ""
    for msg in request.history[-10:]:  # Giữ 10 tin nhắn gần nhất
        role = "Người dùng" if msg.role == "user" else "Trợ lý"
        conversation += f"{role}: {msg.content}\n\n"
    
    # Add current message
    conversation += f"Người dùng: {request.message}\n\n"
    
    # Add context if provided
    context_note = ""
    if request.context:
        context_note = f"\n[Ngữ cảnh: {request.context}]\n"
    
    full_prompt = f"{context_note}{conversation}Trợ lý:"
    
    try:
        # Gọi Gemini API
        result = await gemini.generate_content(
            prompt=full_prompt,
            system_instruction=CHAT_SYSTEM_PROMPT,
            max_tokens=2048,  # Giới hạn cho chat
            temperature=0.7,
        )
        
        reply = result.get("content", "Xin lỗi, tôi không thể trả lời lúc này.")
        tokens = result.get("tokens_output", 0)
        
        return ChatResponse(reply=reply, tokens_used=tokens)
        
    except Exception as e:
        # Fallback response
        error_msg = str(e)
        
        if "429" in error_msg or "quota" in error_msg.lower():
            return ChatResponse(
                reply="⚠️ Xin lỗi, hệ thống đang quá tải. Vui lòng thử lại sau ít phút.\n\n"
                      "Trong khi chờ đợi, bạn có thể:\n"
                      "- Sử dụng các nút tác vụ nhanh bên dưới\n"
                      "- Đọc hướng dẫn sử dụng",
                tokens_used=0
            )
        
        return ChatResponse(
            reply=f"❌ Đã xảy ra lỗi: {error_msg[:100]}...\n\nVui lòng thử lại.",
            tokens_used=0
        )


@router.post("/quick-answer")
async def quick_answer(
    question: str,
    current_user: User = Depends(get_current_user),
):
    """
    Trả lời nhanh các câu hỏi phổ biến (không cần history).
    """
    gemini = get_gemini_service()
    
    try:
        result = await gemini.generate_content(
            prompt=question,
            system_instruction=CHAT_SYSTEM_PROMPT,
            max_tokens=1024,
            temperature=0.5,
        )
        
        return {"answer": result.get("content", "Không có câu trả lời.")}
        
    except Exception as e:
        return {"answer": f"Lỗi: {str(e)[:100]}"}
