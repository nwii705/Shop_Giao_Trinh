"""
Seed database with demo data.
Run: python seed_data.py
"""
import asyncio
import sys
sys.path.insert(0, '.')

from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from app.database.database import AsyncSessionLocal, init_db
from app.database.models import Organization, User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def seed():
    """Create demo organization and user."""
    # Initialize database
    await init_db()
    
    async with AsyncSessionLocal() as db:
        # Check if demo org exists
        from sqlalchemy import select
        
        result = await db.execute(
            select(Organization).where(Organization.code == "DEMO")
        )
        org = result.scalar_one_or_none()
        
        if not org:
            # Create demo organization
            org = Organization(
                name="Trường THCS Demo",
                code="DEMO",
                plan="premium",
                max_users=100,
                quota_monthly=500,
                quota_used=0,
                is_active=True,
            )
            db.add(org)
            await db.flush()
            print(f"✓ Created organization: {org.name} (ID: {org.id})")
        else:
            print(f"→ Organization exists: {org.name}")
        
        # Check if demo user exists
        result = await db.execute(
            select(User).where(User.email == "demo@giaotrinh.ai")
        )
        user = result.scalar_one_or_none()
        
        if not user:
            # Create demo user
            hashed_password = pwd_context.hash("demo123456")
            user = User(
                email="demo@giaotrinh.ai",
                hashed_password=hashed_password,
                full_name="Giáo viên Demo",
                organization_id=org.id,
                is_active=True,
                is_admin=False,
            )
            db.add(user)
            print(f"✓ Created user: {user.email}")
        else:
            print(f"→ User exists: {user.email}")
        
        # Create admin user
        result = await db.execute(
            select(User).where(User.email == "admin@giaotrinh.ai")
        )
        admin = result.scalar_one_or_none()
        
        if not admin:
            hashed_password = pwd_context.hash("admin123456")
            admin = User(
                email="admin@giaotrinh.ai",
                hashed_password=hashed_password,
                full_name="Admin",
                organization_id=org.id,
                is_active=True,
                is_admin=True,
            )
            db.add(admin)
            print(f"✓ Created admin: {admin.email}")
        else:
            print(f"→ Admin exists: {admin.email}")
        
        await db.commit()
        
    print("\n" + "="*50)
    print("Demo accounts created successfully!")
    print("="*50)
    print("\n📧 Demo User:")
    print("   Email: demo@giaotrinh.ai")
    print("   Password: demo123456")
    print("\n👤 Admin:")
    print("   Email: admin@giaotrinh.ai")
    print("   Password: admin123456")
    print("="*50)


if __name__ == "__main__":
    asyncio.run(seed())
