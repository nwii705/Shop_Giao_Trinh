"""
SKKN Router - Sáng kiến Kinh nghiệm API.
Sử dụng Chain-of-Thought prompting cho văn bản dài.
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from typing import List
import asyncio

from app.database.database import get_db
from app.database.models import User, Document, DocumentType
from app.schemas import (
    SKKNRequest, SKKNStep, 
    SKKNIdeationResponse, SKKNOutlineResponse, 
    SKKNContentResponse, SKKNFullResponse
)
from app.auth import get_current_user
from app.services.gemini_service import GeminiService, get_gemini_service
from app.services.document_service import DocumentConverter
from app.services.quota_service import QuotaManager
from app.config import get_settings

settings = get_settings()
router = APIRouter()


@router.post("/ideation", response_model=SKKNIdeationResponse)
async def generate_topics(
    request: SKKNRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Bước 1: Đề xuất 5 đề tài SKKN.
    Dùng Flash-8B để tiết kiệm chi phí (tác vụ đơn giản).
    """
    # Kiểm tra quota
    quota_manager = QuotaManager(db)
    await quota_manager.check_and_consume_quota(
        organization_id=current_user.organization_id,
        user_id=current_user.id,
        action="skkn_ideation",
    )
    
    # Gọi AI
    gemini = get_gemini_service()
    result = await gemini.generate_skkn_ideation(
        subject=request.subject.value,
        grade=request.grade,
        problem=request.problem,
        school_context=request.school_context or "",
    )
    
    # Parse kết quả thành structured data
    content = result["content"]
    
    return SKKNIdeationResponse(
        topics=parse_topics_from_markdown(content),
        recommendation=extract_recommendation(content),
    )


@router.post("/outline", response_model=SKKNOutlineResponse)
async def generate_outline(
    request: SKKNRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Bước 2: Lập dàn ý chi tiết 3 cấp.
    """
    if not request.selected_topic:
        raise HTTPException(
            status_code=400,
            detail="Cần cung cấp selected_topic (đề tài đã chọn)"
        )
    
    quota_manager = QuotaManager(db)
    await quota_manager.check_and_consume_quota(
        organization_id=current_user.organization_id,
        user_id=current_user.id,
        action="skkn_outline",
    )
    
    gemini = get_gemini_service()
    result = await gemini.generate_skkn_outline(
        topic=request.selected_topic,
        subject=request.subject.value,
        school_context=request.school_context or "",
    )
    
    return SKKNOutlineResponse(
        topic=request.selected_topic,
        outline=result["content"],
        estimated_pages=estimate_pages(result["content"]),
    )


@router.post("/section")
async def generate_section(
    request: SKKNRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Bước 3: Viết nội dung từng phần.
    Gọi nhiều lần với section_to_write khác nhau.
    """
    if not request.selected_topic or not request.outline or not request.section_to_write:
        raise HTTPException(
            status_code=400,
            detail="Cần cung cấp selected_topic, outline và section_to_write"
        )
    
    quota_manager = QuotaManager(db)
    await quota_manager.check_and_consume_quota(
        organization_id=current_user.organization_id,
        user_id=current_user.id,
        action="skkn_section",
    )
    
    gemini = get_gemini_service()
    result = await gemini.generate_skkn_section(
        topic=request.selected_topic,
        outline=request.outline,
        section_title=request.section_to_write,
        school_context=request.school_context or "",
    )
    
    return SKKNContentResponse(
        section_title=request.section_to_write,
        content=result["content"],
        word_count=len(result["content"].split()),
    )


@router.post("/full", response_model=SKKNFullResponse)
async def generate_full_skkn(
    request: SKKNRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Tạo SKKN hoàn chỉnh (5 bước tự động).
    
    Quy trình:
    1. Ideation -> Chọn đề tài tốt nhất
    2. Outline -> Lập dàn ý
    3. Content -> Viết từng phần (loop)
    4. Data -> Tạo số liệu
    5. References -> Tài liệu tham khảo
    
    ⚠️ Tốn nhiều quota (5-10 lần gọi AI)
    """
    # Kiểm tra quota cho full SKKN (ước tính 8 lần gọi)
    quota_manager = QuotaManager(db)
    quota_status = await quota_manager.get_quota_status(current_user.organization_id)
    
    if quota_status["quota_remaining"] < 8:
        raise HTTPException(
            status_code=429,
            detail={
                "error": "Không đủ quota để tạo SKKN hoàn chỉnh",
                "required": 8,
                "remaining": quota_status["quota_remaining"],
            }
        )
    
    gemini = get_gemini_service()
    start_time = datetime.utcnow()
    total_tokens = 0
    full_content_parts = []
    
    # === BƯỚC 1: Ideation ===
    await quota_manager.check_and_consume_quota(
        current_user.organization_id, current_user.id, "skkn_step1"
    )
    ideation_result = await gemini.generate_skkn_ideation(
        subject=request.subject.value,
        grade=request.grade,
        problem=request.problem,
        school_context=request.school_context or "",
    )
    total_tokens += ideation_result["tokens_input"] + ideation_result["tokens_output"]
    
    # Chọn đề tài đầu tiên (hoặc có thể parse và chọn theo recommendation)
    selected_topic = request.selected_topic or extract_first_topic(ideation_result["content"])
    
    # === BƯỚC 2: Outline ===
    await quota_manager.check_and_consume_quota(
        current_user.organization_id, current_user.id, "skkn_step2"
    )
    outline_result = await gemini.generate_skkn_outline(
        topic=selected_topic,
        subject=request.subject.value,
        school_context=request.school_context or "",
    )
    total_tokens += outline_result["tokens_input"] + outline_result["tokens_output"]
    outline = outline_result["content"]
    
    # === BƯỚC 3: Content - Viết từng phần ===
    sections = [
        "PHẦN I: MỞ ĐẦU",
        "1. Cơ sở lý luận",
        "2. Thực trạng vấn đề",
        "3. Các biện pháp thực hiện",
        "4. Hiệu quả của sáng kiến",
        "PHẦN III: KẾT LUẬN VÀ KIẾN NGHỊ",
    ]
    
    previous_content = ""
    for section in sections:
        await quota_manager.check_and_consume_quota(
            current_user.organization_id, current_user.id, "skkn_step3"
        )
        section_result = await gemini.generate_skkn_section(
            topic=selected_topic,
            outline=outline,
            section_title=section,
            previous_content=previous_content[-3000:],  # Last 3000 chars for context
            school_context=request.school_context or "",
        )
        total_tokens += section_result["tokens_input"] + section_result["tokens_output"]
        
        full_content_parts.append(f"\n\n{section_result['content']}")
        previous_content += section_result["content"]
    
    # Combine all content
    full_content = f"# {selected_topic}\n\n" + "\n".join(full_content_parts)
    
    # === Lưu vào database ===
    generation_time_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
    
    document = Document(
        organization_id=current_user.organization_id,
        user_id=current_user.id,
        doc_type=DocumentType.SKKN,
        title=selected_topic,
        subject=request.subject.value,
        grade=request.grade,
        lesson_name=selected_topic,
        markdown_content=full_content,
        tokens_input=total_tokens // 2,  # Approximate split
        tokens_output=total_tokens // 2,
        generation_time_ms=generation_time_ms,
        status="completed",
    )
    
    db.add(document)
    await db.flush()
    await db.refresh(document)
    
    # Convert to Word in background
    background_tasks.add_task(
        create_skkn_word_document,
        document.id,
        full_content,
        selected_topic,
    )
    
    return SKKNFullResponse(
        id=document.id,
        topic=selected_topic,
        full_content=full_content,
        download_url=f"/api/skkn/{document.id}/download",
        total_words=len(full_content.split()),
        tokens_used=total_tokens,
        generation_time_ms=generation_time_ms,
        created_at=document.created_at,
    )


@router.get("/{document_id}/download")
async def download_skkn(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Tải file Word của SKKN."""
    result = await db.execute(
        select(Document).where(
            Document.id == document_id,
            Document.organization_id == current_user.organization_id,
            Document.doc_type == DocumentType.SKKN,
        )
    )
    document = result.scalar_one_or_none()
    
    if not document:
        raise HTTPException(status_code=404, detail="Không tìm thấy SKKN")
    
    if not document.file_path:
        # Tạo file nếu chưa có
        converter = DocumentConverter()
        file_path = await converter.convert_markdown_to_docx(
            markdown_content=document.markdown_content,
            output_filename=f"SKKN_{document.title[:50]}",
        )
        document.file_path = file_path
        await db.flush()
    
    return FileResponse(
        path=document.file_path,
        filename=f"SKKN_{document.title[:50]}.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


# ============== HELPER FUNCTIONS ==============

def parse_topics_from_markdown(content: str) -> List[dict]:
    """Parse đề tài từ Markdown response."""
    topics = []
    current_topic = {}
    
    for line in content.split("\n"):
        if line.startswith("## Đề tài"):
            if current_topic:
                topics.append(current_topic)
            title = line.replace("## ", "").split(":")[1].strip() if ":" in line else line.replace("## ", "")
            current_topic = {"title": title, "urgency_analysis": "", "novelty_score": ""}
        elif "Tính cấp thiết" in line:
            current_topic["urgency_analysis"] = line.split(":")[-1].strip()
        elif "Điểm mới" in line:
            current_topic["novelty_score"] = line.split(":")[-1].strip()
    
    if current_topic:
        topics.append(current_topic)
    
    return topics[:5]  # Max 5 topics


def extract_recommendation(content: str) -> str:
    """Trích xuất phần khuyến nghị."""
    if "## Khuyến nghị" in content:
        return content.split("## Khuyến nghị")[1].strip()[:500]
    return "Vui lòng xem xét các đề tài trên và chọn phù hợp với bối cảnh trường học."


def extract_first_topic(content: str) -> str:
    """Lấy đề tài đầu tiên từ kết quả ideation."""
    for line in content.split("\n"):
        if line.startswith("## Đề tài 1:"):
            return line.replace("## Đề tài 1:", "").strip()
    return "Sáng kiến kinh nghiệm"


def estimate_pages(outline: str) -> int:
    """Ước tính số trang dựa trên dàn ý."""
    sections = outline.count("###")
    return max(15, sections * 2)  # Ước tính 2 trang/section, tối thiểu 15 trang


async def create_skkn_word_document(
    document_id: int,
    markdown_content: str,
    title: str,
):
    """Background task tạo file Word cho SKKN."""
    try:
        converter = DocumentConverter()
        file_path = await converter.convert_markdown_to_docx(
            markdown_content=markdown_content,
            output_filename=f"SKKN_{title[:50]}",
        )
        
        # Update trong database (cần session mới)
        from app.database.database import AsyncSessionLocal
        async with AsyncSessionLocal() as session:
            from sqlalchemy import update
            await session.execute(
                update(Document)
                .where(Document.id == document_id)
                .values(file_path=file_path)
            )
            await session.commit()
            
    except Exception as e:
        print(f"Error creating SKKN Word document: {e}")
