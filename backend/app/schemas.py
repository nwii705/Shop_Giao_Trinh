"""
Pydantic schemas for API request/response.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


# ============== ENUMS ==============
class SubjectType(str, Enum):
    KHTN = "khtn"           # Khoa học Tự nhiên
    NGUVAN = "nguvan"       # Ngữ Văn
    TOAN = "toan"           # Toán
    LICHSU = "lichsu"       # Lịch sử
    DIALY = "dialy"         # Địa lý
    GDCD = "gdcd"           # Giáo dục công dân
    OTHER = "other"


class GradeLevel(int, Enum):
    LOP_6 = 6
    LOP_7 = 7
    LOP_8 = 8
    LOP_9 = 9


# ============== AUTH SCHEMAS ==============
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
    organization_id: Optional[int] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone: Optional[str] = None
    subject: Optional[str] = None
    grade_levels: Optional[List[int]] = [6, 7, 8, 9]


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    subject: Optional[str]
    organization_id: int
    is_admin: bool
    documents_created: int
    
    class Config:
        from_attributes = True


# ============== ORGANIZATION SCHEMAS ==============
class OrganizationCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    code: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    plan: str = "free"


class OrganizationResponse(BaseModel):
    id: int
    name: str
    code: str
    plan: str
    max_users: int
    quota_monthly: int
    quota_used: int
    is_active: bool
    
    class Config:
        from_attributes = True


# ============== KHBD (Kế hoạch bài dạy) SCHEMAS ==============
class TextbookType(str, Enum):
    CTST = "ctst"           # Chân trời sáng tạo
    KNTT = "kntt"           # Kết nối tri thức với cuộc sống
    CD = "cd"               # Cánh diều


class KHBDRequest(BaseModel):
    """Request để tạo Kế hoạch bài dạy."""
    subject: SubjectType = Field(..., description="Môn học")
    grade: int = Field(..., ge=6, le=9, description="Khối lớp (6-9)")
    lesson_name: str = Field(..., min_length=5, max_length=500, description="Tên bài học")
    duration: int = Field(default=1, ge=1, le=5, description="Số tiết")
    textbook: TextbookType = Field(default=TextbookType.CTST, description="Bộ sách giáo khoa")
    
    # Optional context
    week_number: Optional[int] = Field(None, ge=1, le=35, description="Tuần thứ")
    period_number: Optional[int] = Field(None, ge=1, le=140, description="Tiết thứ")
    learning_objectives: Optional[str] = Field(None, description="Yêu cầu cần đạt bổ sung")
    school_context: Optional[str] = Field(None, description="Đặc điểm trường (vùng cao, thiếu thiết bị...)")
    
    # Output options
    include_rubric: bool = Field(default=False, description="Bao gồm phiếu đánh giá")
    output_format: str = Field(default="docx", description="Định dạng: docx, markdown, pdf")


class KHBDResponse(BaseModel):
    """Response sau khi tạo KHBD."""
    id: int
    title: str
    subject: str
    grade: int
    lesson_name: str
    
    # Generated content
    markdown_content: str
    download_url: Optional[str] = None
    
    # Metrics
    tokens_used: int
    generation_time_ms: int
    quota_remaining: int
    
    created_at: datetime


# ============== SKKN (Sáng kiến kinh nghiệm) SCHEMAS ==============
class SKKNStep(str, Enum):
    IDEATION = "ideation"       # Bước 1: Đề xuất đề tài
    OUTLINE = "outline"         # Bước 2: Lập dàn ý
    CONTENT = "content"         # Bước 3: Viết nội dung
    DATA = "data"               # Bước 4: Tạo số liệu
    REFERENCES = "references"   # Bước 5: Tài liệu tham khảo
    FULL = "full"               # Tạo toàn bộ (multi-step tự động)


class SKKNRequest(BaseModel):
    """Request để tạo Sáng kiến kinh nghiệm."""
    step: SKKNStep = Field(default=SKKNStep.FULL, description="Bước xử lý")
    
    # Context
    subject: SubjectType = Field(..., description="Môn học")
    grade: int = Field(..., ge=6, le=9, description="Khối lớp")
    problem: str = Field(..., min_length=20, description="Vấn đề cần giải quyết")
    
    # For step-by-step
    selected_topic: Optional[str] = Field(None, description="Đề tài đã chọn (cho bước 2+)")
    outline: Optional[str] = Field(None, description="Dàn ý đã có (cho bước 3+)")
    section_to_write: Optional[str] = Field(None, description="Phần cần viết (cho bước 3)")
    
    # School context for personalization
    school_name: Optional[str] = None
    school_context: Optional[str] = Field(
        None, 
        description="Đặc điểm trường (vùng cao, thiếu máy chiếu, HS dân tộc...)"
    )


class SKKNIdeationResponse(BaseModel):
    """Response cho bước 1 - Đề xuất đề tài."""
    topics: List[dict]  # [{title, urgency_analysis, novelty_score}]
    recommendation: str


class SKKNOutlineResponse(BaseModel):
    """Response cho bước 2 - Dàn ý."""
    topic: str
    outline: str  # Markdown format
    estimated_pages: int


class SKKNContentResponse(BaseModel):
    """Response cho bước 3 - Nội dung."""
    section_title: str
    content: str  # Markdown format
    word_count: int


class SKKNFullResponse(BaseModel):
    """Response cho SKKN hoàn chỉnh."""
    id: int
    topic: str
    full_content: str
    download_url: Optional[str] = None
    
    # Metrics
    total_words: int
    tokens_used: int
    generation_time_ms: int
    
    created_at: datetime


# ============== QUOTA & USAGE ==============
class QuotaStatus(BaseModel):
    """Trạng thái quota của organization."""
    organization_id: int
    plan: str
    quota_monthly: int
    quota_used: int
    quota_remaining: int
    reset_date: datetime
    
    # Cost estimate
    cost_this_month_vnd: int
    documents_created: int


class UsageStats(BaseModel):
    """Thống kê sử dụng cho admin."""
    period: str  # "2026-01", "2026-01-23"
    total_documents: int
    by_type: dict  # {"khbd_khtn": 50, "skkn": 10}
    total_tokens: int
    estimated_cost_usd: float
    active_users: int
