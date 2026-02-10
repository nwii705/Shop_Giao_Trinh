"""
Authentication Router - Đăng nhập, đăng ký.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta

from app.database.database import get_db
from app.database.models import User, Organization
from app.schemas import UserCreate, UserResponse, Token, UserLogin
from app.auth import (
    verify_password, 
    get_password_hash, 
    create_access_token,
    get_current_user,
)
from app.config import get_settings

settings = get_settings()
router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """
    Đăng nhập và nhận JWT token.
    
    - **username**: Email đăng nhập
    - **password**: Mật khẩu
    """
    # Tìm user theo email
    result = await db.execute(
        select(User).where(User.email == form_data.username)
    )
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không đúng",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản đã bị vô hiệu hóa"
        )
    
    # Tạo access token
    access_token = create_access_token(
        data={
            "user_id": user.id,
            "organization_id": user.organization_id,
            "is_admin": user.is_admin,
        },
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return Token(access_token=access_token)


@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserCreate,
    organization_code: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Đăng ký tài khoản mới.
    Cần mã tổ chức (organization_code) từ admin.
    """
    # Kiểm tra organization
    result = await db.execute(
        select(Organization).where(Organization.code == organization_code)
    )
    org = result.scalar_one_or_none()
    
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mã tổ chức không hợp lệ"
        )
    
    if not org.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tổ chức đã bị vô hiệu hóa"
        )
    
    # Kiểm tra số lượng user
    result = await db.execute(
        select(User).where(User.organization_id == org.id)
    )
    current_users = len(result.scalars().all())
    
    if current_users >= org.max_users:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Tổ chức đã đạt giới hạn {org.max_users} tài khoản. Liên hệ admin để nâng cấp."
        )
    
    # Kiểm tra email đã tồn tại
    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email đã được sử dụng"
        )
    
    # Tạo user mới
    new_user = User(
        organization_id=org.id,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        full_name=user_data.full_name,
        phone=user_data.phone,
        subject=user_data.subject,
        grade_levels=user_data.grade_levels,
    )
    
    db.add(new_user)
    await db.flush()
    await db.refresh(new_user)
    
    return UserResponse.model_validate(new_user)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Lấy thông tin user hiện tại."""
    return UserResponse.model_validate(current_user)
