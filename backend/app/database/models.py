"""
Database models for B2B SaaS application.
Multi-tenant architecture: Organization -> Users -> Documents
"""
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, 
    ForeignKey, Enum as SQLEnum, JSON
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
from datetime import datetime
import enum

Base = declarative_base()


class PlanType(str, enum.Enum):
    """Subscription plan types."""
    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"


class DocumentType(str, enum.Enum):
    """Types of generated documents."""
    KHBD_KHTN = "khbd_khtn"      # Kế hoạch bài dạy KHTN
    KHBD_NGUVAN = "khbd_nguvan"  # Kế hoạch bài dạy Ngữ Văn
    KHBD_TOAN = "khbd_toan"      # Kế hoạch bài dạy Toán
    KHBD_OTHER = "khbd_other"    # Các môn khác
    SKKN = "skkn"                # Sáng kiến kinh nghiệm


class Organization(Base):
    """
    Doanh nghiệp/Trường học - Đơn vị mua tài khoản.
    Mô hình B2B: Bán theo số lượng người dùng.
    """
    __tablename__ = "organizations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)  # Tên trường/Sở GD
    code = Column(String(50), unique=True, index=True)  # Mã đơn vị
    email = Column(String(255), unique=True, index=True)
    phone = Column(String(20))
    address = Column(Text)
    
    # Subscription
    plan = Column(SQLEnum(PlanType), default=PlanType.FREE)
    max_users = Column(Integer, default=5)  # Số tài khoản tối đa
    quota_monthly = Column(Integer, default=10)  # Quota tổng/tháng
    quota_used = Column(Integer, default=0)  # Đã dùng trong tháng
    quota_reset_date = Column(DateTime, default=func.now())
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # API Key riêng cho Enterprise
    api_key = Column(String(255), unique=True, nullable=True)
    
    # Relationships
    users = relationship("User", back_populates="organization")
    documents = relationship("Document", back_populates="organization")


class User(Base):
    """Giáo viên - Người dùng cuối."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    phone = Column(String(20))
    
    # Teacher Info
    subject = Column(String(100))  # Môn dạy chính
    grade_levels = Column(JSON)    # Các khối lớp: [6, 7, 8, 9]
    
    # Usage tracking
    documents_created = Column(Integer, default=0)
    last_activity = Column(DateTime)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)  # Admin của organization
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    organization = relationship("Organization", back_populates="users")
    documents = relationship("Document", back_populates="user")


class Document(Base):
    """Tài liệu đã tạo - Để tracking và cache."""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Document Info
    doc_type = Column(SQLEnum(DocumentType), nullable=False)
    title = Column(String(500))
    subject = Column(String(100))  # Môn học
    grade = Column(Integer)        # Lớp
    lesson_name = Column(String(500))  # Tên bài
    duration = Column(Integer)     # Số tiết
    
    # Content
    prompt_used = Column(Text)     # Prompt đã dùng (để debug)
    markdown_content = Column(Text)  # Nội dung Markdown
    file_path = Column(String(500))  # Đường dẫn file Word
    
    # AI Metrics
    tokens_input = Column(Integer, default=0)
    tokens_output = Column(Integer, default=0)
    generation_time_ms = Column(Integer, default=0)
    
    # Status
    status = Column(String(50), default="completed")  # pending, completed, failed
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    organization = relationship("Organization", back_populates="documents")
    user = relationship("User", back_populates="documents")


class UsageLog(Base):
    """Log sử dụng để tính billing và analytics."""
    __tablename__ = "usage_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    action = Column(String(100))  # generate_khbd, generate_skkn, download
    doc_type = Column(String(50))
    tokens_used = Column(Integer, default=0)
    cost_usd = Column(Integer, default=0)  # Micro USD (x1,000,000)
    
    created_at = Column(DateTime, default=func.now())
