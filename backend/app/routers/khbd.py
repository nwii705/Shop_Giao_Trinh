"""
KHBD Router - Kế hoạch Bài dạy API.
Core feature của ứng dụng.
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import os

from app.database.database import get_db
from app.database.models import User, Document, DocumentType
from app.schemas import KHBDRequest, KHBDResponse, SubjectType
from app.auth import get_current_user
from app.services.gemini_service import GeminiService, get_gemini_service
from app.services.document_service import DocumentConverter
from app.services.quota_service import QuotaManager
from app.prompts.templates import get_system_prompt, build_user_prompt
from app.config import get_settings

settings = get_settings()
router = APIRouter()

# Import demo generator
from app.services.demo_generator import generate_khtn_demo_content, generate_nguvan_demo_content


def generate_demo_khbd(request: KHBDRequest) -> dict:
    """Generate demo KHBD content based on actual curriculum data."""
    
    # Lấy thông tin bộ sách
    textbook = getattr(request, 'textbook', None)
    textbook_code = textbook.value if textbook else "ctst"
    
    # Chọn generator theo môn
    if request.subject.value == "nguvan":
        demo_content = generate_nguvan_demo_content(
            lesson_name=request.lesson_name,
            grade=request.grade,
            duration=request.duration,
            textbook=textbook_code,
            period_number=request.period_number,
            week_number=request.week_number,
        )
    else:
        demo_content = generate_khtn_demo_content(
            lesson_name=request.lesson_name,
            grade=request.grade,
            duration=request.duration,
            textbook=textbook_code,
            period_number=request.period_number,
            week_number=request.week_number,
        )
    
    return {
        "content": demo_content,
        "tokens_input": 0,
        "tokens_output": len(demo_content.split()),
        "generation_time_ms": 100,
    }


@router.post("/generate", response_model=KHBDResponse)
async def generate_khbd(
    request: KHBDRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Tạo Kế hoạch Bài dạy (KHBD).
    
    - Sử dụng Gemini 1.5 Flash để tối ưu chi phí
    - Output: Markdown với LaTeX cho công thức
    - Tự động trừ quota theo gói doanh nghiệp
    """
    # 1. Kiểm tra và trừ quota
    quota_manager = QuotaManager(db)
    quota_result = await quota_manager.check_and_consume_quota(
        organization_id=current_user.organization_id,
        user_id=current_user.id,
        action="generate_khbd",
    )
    
    # 2. Lấy system prompt phù hợp
    subject_name = request.subject.value
    system_prompt = get_system_prompt(subject_name)
    
    # 3. Build user prompt
    user_prompt = build_user_prompt(
        subject=subject_name,
        grade=request.grade,
        lesson_name=request.lesson_name,
        duration=request.duration,
        textbook=request.textbook.value if request.textbook else "ctst",
        week_number=request.week_number,
        period_number=request.period_number,
        learning_objectives=request.learning_objectives,
        school_context=request.school_context,
    )
    
    # 4. Gọi Gemini API
    gemini = get_gemini_service()
    
    try:
        # Kiểm tra DEMO_MODE
        if settings.DEMO_MODE or not settings.GEMINI_API_KEY:
            result = generate_demo_khbd(request)
        else:
            result = await gemini.generate_content(
                prompt=user_prompt,
                system_instruction=system_prompt,
            )
    except Exception as e:
        # Fallback to demo mode on error
        if settings.DEMO_MODE:
            result = generate_demo_khbd(request)
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Lỗi khi tạo nội dung: {str(e)}"
            )
    
    # 5. Map subject to document type
    doc_type_map = {
        SubjectType.KHTN: DocumentType.KHBD_KHTN,
        SubjectType.NGUVAN: DocumentType.KHBD_NGUVAN,
        SubjectType.TOAN: DocumentType.KHBD_TOAN,
    }
    doc_type = doc_type_map.get(request.subject, DocumentType.KHBD_OTHER)
    
    # 6. Lưu document vào database
    document = Document(
        organization_id=current_user.organization_id,
        user_id=current_user.id,
        doc_type=doc_type,
        title=f"KHBD - {request.lesson_name}",
        subject=subject_name,
        grade=request.grade,
        lesson_name=request.lesson_name,
        duration=request.duration,
        prompt_used=user_prompt[:2000],  # Truncate for storage
        markdown_content=result["content"],
        tokens_input=result["tokens_input"],
        tokens_output=result["tokens_output"],
        generation_time_ms=result["generation_time_ms"],
        status="completed",
    )
    
    db.add(document)
    await db.flush()
    await db.refresh(document)
    
    # 7. Update user stats
    current_user.documents_created += 1
    current_user.last_activity = datetime.utcnow()
    
    # 8. Convert to Word in background (if requested)
    download_url = None
    if request.output_format == "docx":
        # Tạo file Word async
        background_tasks.add_task(
            create_word_document,
            document.id,
            result["content"],
            request.lesson_name,
            db,
        )
    
    return KHBDResponse(
        id=document.id,
        title=document.title,
        subject=subject_name,
        grade=request.grade,
        lesson_name=request.lesson_name,
        markdown_content=result["content"],
        download_url=download_url,
        tokens_used=result["tokens_input"] + result["tokens_output"],
        generation_time_ms=result["generation_time_ms"],
        quota_remaining=quota_result["quota_remaining"],
        created_at=document.created_at,
    )


@router.get("/{document_id}/download")
async def download_khbd(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Tải file Word của KHBD đã tạo.
    """
    from sqlalchemy import select
    
    result = await db.execute(
        select(Document).where(
            Document.id == document_id,
            Document.organization_id == current_user.organization_id,
        )
    )
    document = result.scalar_one_or_none()
    
    if not document:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài liệu")
    
    if not document.file_path or not os.path.exists(document.file_path):
        # Tạo file nếu chưa có
        converter = DocumentConverter()
        file_path = await converter.convert_markdown_to_docx(
            markdown_content=document.markdown_content,
            output_filename=f"KHBD_{document.lesson_name}",
        )
        document.file_path = file_path
        await db.flush()
    
    return FileResponse(
        path=document.file_path,
        filename=f"KHBD_{document.lesson_name}.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


@router.get("/history")
async def get_history(
    limit: int = 20,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Lấy lịch sử KHBD đã tạo.
    """
    from sqlalchemy import select
    
    result = await db.execute(
        select(Document)
        .where(
            Document.user_id == current_user.id,
            Document.doc_type.in_([
                DocumentType.KHBD_KHTN,
                DocumentType.KHBD_NGUVAN,
                DocumentType.KHBD_OTHER,
            ])
        )
        .order_by(Document.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    documents = result.scalars().all()
    
    return {
        "total": len(documents),
        "items": [
            {
                "id": doc.id,
                "title": doc.title,
                "subject": doc.subject,
                "grade": doc.grade,
                "lesson_name": doc.lesson_name,
                "created_at": doc.created_at.isoformat(),
            }
            for doc in documents
        ]
    }


async def create_word_document(
    document_id: int,
    markdown_content: str,
    lesson_name: str,
    db: AsyncSession,
):
    """Background task để tạo file Word."""
    try:
        converter = DocumentConverter()
        file_path = await converter.convert_markdown_to_docx(
            markdown_content=markdown_content,
            output_filename=f"KHBD_{lesson_name}",
        )
        
        # Update database
        from sqlalchemy import update
        await db.execute(
            update(Document)
            .where(Document.id == document_id)
            .values(file_path=file_path)
        )
        await db.commit()
        
    except Exception as e:
        print(f"Error creating Word document: {e}")


from pydantic import BaseModel

class ConvertToWordRequest(BaseModel):
    """Request để convert markdown thành Word."""
    markdown_content: str
    filename: str = "document"


@router.post("/convert-to-word")
async def convert_to_word(
    request: ConvertToWordRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Convert markdown content thành file Word và trả về file.
    Dùng cho nút download trong chat.
    """
    try:
        converter = DocumentConverter()
        file_path = await converter.convert_markdown_to_docx(
            markdown_content=request.markdown_content,
            output_filename=request.filename,
        )
        
        safe_filename = request.filename.replace(" ", "_")[:50]
        
        return FileResponse(
            path=file_path,
            filename=f"{safe_filename}.docx",
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi tạo file Word: {str(e)}")
