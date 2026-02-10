"""
Configuration settings for the application.
Mô hình B2B SaaS - Bán tài khoản cho doanh nghiệp (trường học, Sở GD&ĐT)
"""
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings  # Fallback for older pydantic

from typing import Optional
from functools import lru_cache
import os


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # App Info
    APP_NAME: str = "GiaoTrinh AI - Hỗ trợ Giáo viên"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    DEMO_MODE: bool = False  # Tắt demo mode để dùng Gemini API thực
    
    # Database - SQLite mặc định cho development, PostgreSQL cho production
    DATABASE_URL: str = "sqlite+aiosqlite:///./giaotrinh.db"
    
    # Gemini AI - Sử dụng Flash để tối ưu chi phí
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.0-flash"  # Model mới nhất, chi phí thấp
    GEMINI_MODEL_SIMPLE: str = "gemini-2.0-flash"  # Cho tác vụ đơn giản
    
    # AI Generation Settings
    AI_TEMPERATURE: float = 0.7  # Cân bằng giữa sáng tạo và nhất quán
    AI_MAX_OUTPUT_TOKENS: int = 8192
    
    # JWT Authentication
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Rate Limiting (requests per minute)
    RATE_LIMIT_FREE: int = 5
    RATE_LIMIT_BASIC: int = 30
    RATE_LIMIT_PREMIUM: int = 100
    RATE_LIMIT_ENTERPRISE: int = 500
    
    # File Paths
    TEMPLATE_DIR: str = "templates"
    OUTPUT_DIR: str = "outputs"
    REFERENCE_DOCX: str = "templates/reference.docx"
    
    # Pricing Tiers (số giáo án/tháng)
    QUOTA_FREE: int = 10
    QUOTA_BASIC: int = 100
    QUOTA_PREMIUM: int = 500
    QUOTA_ENTERPRISE: int = 5000  # Unlimited thực tế
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields in .env


@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()


# Pricing Plans cho B2B
PRICING_PLANS = {
    "free": {
        "name": "Dùng thử",
        "price_vnd": 0,
        "quota_monthly": 10,
        "rate_limit": 5,
        "features": ["KHBD cơ bản", "2 môn học"],
    },
    "basic": {
        "name": "Cơ bản",
        "price_vnd": 199000,  # ~8 USD/tháng
        "quota_monthly": 100,
        "rate_limit": 30,
        "features": ["KHBD đầy đủ", "Tất cả môn học", "Xuất Word"],
    },
    "premium": {
        "name": "Nâng cao",
        "price_vnd": 499000,  # ~20 USD/tháng
        "quota_monthly": 500,
        "rate_limit": 100,
        "features": ["Tất cả tính năng Basic", "SKKN", "Ưu tiên xử lý"],
    },
    "enterprise": {
        "name": "Doanh nghiệp",
        "price_vnd": "Liên hệ",  # Custom pricing
        "quota_monthly": 5000,
        "rate_limit": 500,
        "features": [
            "Tất cả tính năng Premium",
            "API riêng",
            "Hỗ trợ 24/7",
            "Custom template",
            "Quản lý nhiều tài khoản",
        ],
    },
}
