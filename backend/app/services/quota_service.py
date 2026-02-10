"""
Quota Management Service - Quản lý hạn mức sử dụng cho B2B.
"""
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from fastapi import HTTPException, status

from app.database.models import Organization, User, UsageLog, PlanType
from app.config import get_settings, PRICING_PLANS

settings = get_settings()


class QuotaManager:
    """
    Quản lý quota theo gói doanh nghiệp.
    
    Flow:
    1. Khi user request -> check_and_consume_quota()
    2. Nếu đủ quota -> trừ quota, log usage
    3. Nếu hết quota -> raise exception
    4. Hàng tháng: reset_monthly_quota()
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def check_and_consume_quota(
        self,
        organization_id: int,
        user_id: int,
        action: str = "generate_khbd",
        tokens_used: int = 0,
    ) -> dict:
        """
        Kiểm tra và trừ quota.
        
        Args:
            organization_id: ID tổ chức
            user_id: ID người dùng
            action: Loại hành động
            tokens_used: Số token đã dùng (để tính cost)
            
        Returns:
            {"quota_remaining": int, "cost_usd": float}
            
        Raises:
            HTTPException 429 nếu hết quota
        """
        # Lấy thông tin organization
        result = await self.db.execute(
            select(Organization).where(Organization.id == organization_id)
        )
        org = result.scalar_one_or_none()
        
        if not org:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy tổ chức"
            )
        
        # Kiểm tra cần reset quota không
        await self._check_quota_reset(org)
        
        # Kiểm tra còn quota không
        if org.quota_used >= org.quota_monthly:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "Đã hết quota tháng này",
                    "quota_monthly": org.quota_monthly,
                    "quota_used": org.quota_used,
                    "reset_date": org.quota_reset_date.isoformat(),
                    "upgrade_url": "/api/subscription/upgrade"
                }
            )
        
        # Trừ quota
        org.quota_used += 1
        
        # Tính cost
        cost_usd = self._calculate_cost(tokens_used)
        
        # Log usage
        usage_log = UsageLog(
            organization_id=organization_id,
            user_id=user_id,
            action=action,
            tokens_used=tokens_used,
            cost_usd=int(cost_usd * 1_000_000),  # Micro USD
        )
        self.db.add(usage_log)
        
        await self.db.flush()
        
        return {
            "quota_remaining": org.quota_monthly - org.quota_used,
            "cost_usd": cost_usd,
        }
    
    async def get_quota_status(self, organization_id: int) -> dict:
        """Lấy trạng thái quota hiện tại."""
        result = await self.db.execute(
            select(Organization).where(Organization.id == organization_id)
        )
        org = result.scalar_one_or_none()
        
        if not org:
            raise HTTPException(status_code=404, detail="Không tìm thấy tổ chức")
        
        # Đếm số document trong tháng
        # (Simplified - trong production cần query chi tiết hơn)
        
        return {
            "organization_id": org.id,
            "plan": org.plan.value,
            "plan_name": PRICING_PLANS[org.plan.value]["name"],
            "quota_monthly": org.quota_monthly,
            "quota_used": org.quota_used,
            "quota_remaining": org.quota_monthly - org.quota_used,
            "quota_percentage": round((org.quota_used / org.quota_monthly) * 100, 1),
            "reset_date": org.quota_reset_date.isoformat(),
            "is_near_limit": (org.quota_used / org.quota_monthly) > 0.8,
        }
    
    async def upgrade_plan(
        self,
        organization_id: int,
        new_plan: str,
    ) -> dict:
        """
        Nâng cấp gói subscription.
        Trong production: tích hợp payment gateway.
        """
        if new_plan not in PRICING_PLANS:
            raise HTTPException(status_code=400, detail="Gói không hợp lệ")
        
        result = await self.db.execute(
            select(Organization).where(Organization.id == organization_id)
        )
        org = result.scalar_one_or_none()
        
        if not org:
            raise HTTPException(status_code=404, detail="Không tìm thấy tổ chức")
        
        plan_info = PRICING_PLANS[new_plan]
        
        # Cập nhật plan
        org.plan = PlanType(new_plan)
        org.quota_monthly = plan_info["quota_monthly"]
        
        # Thêm quota bonus khi upgrade
        bonus_quota = plan_info["quota_monthly"] - org.quota_used
        if bonus_quota > 0:
            org.quota_used = 0  # Reset về 0 khi upgrade
        
        await self.db.flush()
        
        return {
            "success": True,
            "new_plan": new_plan,
            "quota_monthly": org.quota_monthly,
            "message": f"Đã nâng cấp lên gói {plan_info['name']}"
        }
    
    async def _check_quota_reset(self, org: Organization):
        """Kiểm tra và reset quota nếu đã sang tháng mới."""
        now = datetime.utcnow()
        
        if org.quota_reset_date is None:
            org.quota_reset_date = now
            org.quota_used = 0
        elif now >= org.quota_reset_date + timedelta(days=30):
            # Reset quota hàng tháng
            org.quota_used = 0
            org.quota_reset_date = now
    
    def _calculate_cost(self, tokens: int, model: str = "flash") -> float:
        """
        Tính chi phí USD dựa trên tokens.
        
        Gemini 1.5 Flash pricing:
        - Input: $0.075 / 1M tokens
        - Output: $0.30 / 1M tokens
        
        Giả sử 70% là output tokens (thường output dài hơn input prompt)
        """
        if tokens == 0:
            return 0.0
        
        input_tokens = int(tokens * 0.3)
        output_tokens = int(tokens * 0.7)
        
        if model == "flash":
            input_cost = (input_tokens / 1_000_000) * 0.075
            output_cost = (output_tokens / 1_000_000) * 0.30
        else:  # flash-8b
            input_cost = (input_tokens / 1_000_000) * 0.0375
            output_cost = (output_tokens / 1_000_000) * 0.15
        
        return round(input_cost + output_cost, 6)


# ============== Rate Limiting ==============

def get_rate_limit_for_plan(plan: str) -> int:
    """Lấy rate limit (requests/minute) cho từng gói."""
    limits = {
        "free": settings.RATE_LIMIT_FREE,
        "basic": settings.RATE_LIMIT_BASIC,
        "premium": settings.RATE_LIMIT_PREMIUM,
        "enterprise": settings.RATE_LIMIT_ENTERPRISE,
    }
    return limits.get(plan, settings.RATE_LIMIT_FREE)
