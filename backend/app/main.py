"""
FastAPI Main Application - Entry point.
B2B SaaS cho Giáo viên - Hỗ trợ soạn KHBD và SKKN.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from app.config import get_settings
from app.database.database import init_db
from app.routers import auth, khbd, skkn, organizations, chat

settings = get_settings()

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown."""
    # Startup
    logger.info("Khởi động ứng dụng...")
    try:
        await init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.error(f"Database init error: {e}")
    
    yield
    
    # Shutdown
    logger.info("Đang tắt ứng dụng...")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="""
## API Hỗ trợ Giáo viên soạn Kế hoạch Bài dạy và Sáng kiến Kinh nghiệm

### Tính năng chính:
- 📚 **KHBD (Kế hoạch bài dạy)**: Soạn giáo án theo Công văn 5512
- 🔬 **KHTN**: Hỗ trợ công thức Hóa học, Vật lý, Sinh học (LaTeX)
- 📖 **Ngữ Văn**: Phân tích văn bản, câu hỏi mở
- 💡 **SKKN**: Sáng kiến kinh nghiệm với quy trình 5 bước
- 📄 **Export Word**: Xuất file .docx với định dạng chuẩn

### Mô hình B2B:
- Bán tài khoản cho Trường học, Sở GD&ĐT
- Quản lý quota theo gói
- API riêng cho Enterprise
    """,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cấu hình domain cụ thể trong production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== EXCEPTION HANDLERS ==============

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Đã xảy ra lỗi hệ thống",
            "detail": str(exc) if settings.DEBUG else "Vui lòng thử lại sau"
        }
    )


# ============== ROUTERS ==============

app.include_router(
    auth.router,
    prefix="/api/auth",
    tags=["Authentication"]
)

app.include_router(
    khbd.router,
    prefix="/api/khbd",
    tags=["Kế hoạch Bài dạy"]
)

app.include_router(
    skkn.router,
    prefix="/api/skkn",
    tags=["Sáng kiến Kinh nghiệm"]
)

app.include_router(
    organizations.router,
    prefix="/api/organizations",
    tags=["Organizations (Admin)"]
)

app.include_router(
    chat.router,
    prefix="/api/chat",
    tags=["Chat AI"]
)


# ============== ROOT ENDPOINTS ==============

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/api/pricing")
async def get_pricing():
    """Bảng giá các gói dịch vụ."""
    from app.config import PRICING_PLANS
    return {
        "currency": "VND",
        "plans": PRICING_PLANS,
        "note": "Liên hệ để được tư vấn gói Enterprise"
    }


# ============== RUN SERVER ==============

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
