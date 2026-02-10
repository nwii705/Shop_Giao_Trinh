"""
Organizations Router - Quản lý tổ chức (Admin).
B2B: Mỗi trường học/Sở GD là một Organization.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
import secrets

from app.database.database import get_db
from app.database.models import Organization, User, Document, PlanType
from app.schemas import OrganizationCreate, OrganizationResponse, QuotaStatus
from app.auth import get_admin_user, get_current_user
from app.services.quota_service import QuotaManager
from app.config import PRICING_PLANS

router = APIRouter()


@router.post("/", response_model=OrganizationResponse)
async def create_organization(
    org_data: OrganizationCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Tạo tổ chức mới (Trường học, Sở GD&ĐT).
    
    Endpoint này thường được gọi bởi Super Admin hoặc tự động từ hệ thống bán hàng.
    """
    # Kiểm tra code đã tồn tại
    result = await db.execute(
        select(Organization).where(Organization.code == org_data.code)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Mã tổ chức đã tồn tại"
        )
    
    # Kiểm tra email
    result = await db.execute(
        select(Organization).where(Organization.email == org_data.email)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Email đã được sử dụng"
        )
    
    # Lấy thông tin plan
    plan_info = PRICING_PLANS.get(org_data.plan, PRICING_PLANS["free"])
    
    # Tạo organization
    new_org = Organization(
        name=org_data.name,
        code=org_data.code.upper(),
        email=org_data.email,
        phone=org_data.phone,
        address=org_data.address,
        plan=PlanType(org_data.plan),
        max_users=5 if org_data.plan == "free" else (20 if org_data.plan == "basic" else 100),
        quota_monthly=plan_info["quota_monthly"],
        quota_used=0,
    )
    
    # Tạo API key cho Enterprise
    if org_data.plan == "enterprise":
        new_org.api_key = f"gv_{secrets.token_urlsafe(32)}"
    
    db.add(new_org)
    await db.flush()
    await db.refresh(new_org)
    
    return OrganizationResponse.model_validate(new_org)


@router.get("/me", response_model=OrganizationResponse)
async def get_my_organization(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lấy thông tin tổ chức của user hiện tại."""
    result = await db.execute(
        select(Organization).where(Organization.id == current_user.organization_id)
    )
    org = result.scalar_one_or_none()
    
    if not org:
        raise HTTPException(status_code=404, detail="Không tìm thấy tổ chức")
    
    return OrganizationResponse.model_validate(org)


@router.get("/me/quota", response_model=QuotaStatus)
async def get_quota_status(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lấy trạng thái quota của tổ chức."""
    quota_manager = QuotaManager(db)
    status = await quota_manager.get_quota_status(current_user.organization_id)
    
    # Thêm thống kê
    result = await db.execute(
        select(func.count(Document.id))
        .where(Document.organization_id == current_user.organization_id)
    )
    total_docs = result.scalar() or 0
    
    return QuotaStatus(
        organization_id=current_user.organization_id,
        plan=status["plan"],
        quota_monthly=status["quota_monthly"],
        quota_used=status["quota_used"],
        quota_remaining=status["quota_remaining"],
        reset_date=status["reset_date"],
        cost_this_month_vnd=0,  # Calculate from usage logs
        documents_created=total_docs,
    )


@router.get("/me/users")
async def list_organization_users(
    current_user: User = Depends(get_admin_user),  # Only admin
    db: AsyncSession = Depends(get_db),
):
    """Liệt kê users trong tổ chức (Admin only)."""
    result = await db.execute(
        select(User)
        .where(User.organization_id == current_user.organization_id)
        .order_by(User.created_at.desc())
    )
    users = result.scalars().all()
    
    return {
        "total": len(users),
        "users": [
            {
                "id": u.id,
                "email": u.email,
                "full_name": u.full_name,
                "subject": u.subject,
                "documents_created": u.documents_created,
                "is_active": u.is_active,
                "is_admin": u.is_admin,
                "created_at": u.created_at.isoformat(),
            }
            for u in users
        ]
    }


@router.post("/me/users/{user_id}/toggle-admin")
async def toggle_user_admin(
    user_id: int,
    current_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Bật/tắt quyền admin cho user (Admin only)."""
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Không thể thay đổi quyền của chính mình")
    
    result = await db.execute(
        select(User).where(
            User.id == user_id,
            User.organization_id == current_user.organization_id,
        )
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy user")
    
    user.is_admin = not user.is_admin
    await db.flush()
    
    return {"success": True, "is_admin": user.is_admin}


@router.get("/me/stats")
async def get_organization_stats(
    current_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Thống kê sử dụng của tổ chức (Admin only)."""
    org_id = current_user.organization_id
    
    # Đếm users
    result = await db.execute(
        select(func.count(User.id)).where(User.organization_id == org_id)
    )
    total_users = result.scalar() or 0
    
    # Đếm active users (có hoạt động trong 30 ngày)
    from datetime import datetime, timedelta
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    result = await db.execute(
        select(func.count(User.id)).where(
            User.organization_id == org_id,
            User.last_activity >= thirty_days_ago,
        )
    )
    active_users = result.scalar() or 0
    
    # Đếm documents theo loại
    result = await db.execute(
        select(Document.doc_type, func.count(Document.id))
        .where(Document.organization_id == org_id)
        .group_by(Document.doc_type)
    )
    docs_by_type = {str(row[0].value): row[1] for row in result.all()}
    
    # Tổng tokens
    result = await db.execute(
        select(
            func.sum(Document.tokens_input),
            func.sum(Document.tokens_output),
        ).where(Document.organization_id == org_id)
    )
    row = result.one()
    total_tokens = (row[0] or 0) + (row[1] or 0)
    
    # Ước tính chi phí
    estimated_cost_usd = (total_tokens / 1_000_000) * 0.2  # Average cost
    
    return {
        "total_users": total_users,
        "active_users_30d": active_users,
        "documents_by_type": docs_by_type,
        "total_documents": sum(docs_by_type.values()),
        "total_tokens": total_tokens,
        "estimated_cost_usd": round(estimated_cost_usd, 4),
        "estimated_cost_vnd": int(estimated_cost_usd * 25000),
    }
