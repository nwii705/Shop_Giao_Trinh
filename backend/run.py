"""
Script khởi động server - Tự động kiểm tra và cài đặt dependencies.
"""
import subprocess
import sys
import os
import io

# Fix Unicode encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def install_packages():
    """Cài đặt các packages cần thiết."""
    packages = [
        "fastapi",
        "uvicorn[standard]",
        "sqlalchemy",
        "aiosqlite",
        "pydantic-settings",
        "python-jose[cryptography]",
        "passlib[bcrypt]",
        "python-multipart",
        "slowapi",
        "httpx",
        "aiofiles",
    ]
    
    print("📦 Đang cài đặt dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q"] + packages)
    print("✓ Đã cài đặt xong!")

def main():
    # Kiểm tra xem đã cài đủ chưa
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import aiosqlite
    except ImportError:
        install_packages()
    
    # Chạy server
    print("🚀 Khởi động GiaoTrinh AI Backend...")
    print("📖 API Docs: http://localhost:8000/docs")
    print("-" * 50)
    
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
