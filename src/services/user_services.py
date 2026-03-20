from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from fastapi import HTTPException
from uuid import UUID

from src.db.models.user_model import User
from src.schemas.user_schemas import UserCreate, UserUpdate, AdminUserUpdate
from src.utils.auth_utils import generate_password_hash, verify_password


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ---------------- GET USER BY EMAIL ----------------
    async def get_user_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()

    # ---------------- GET USER BY ID ----------------
    async def get_user_by_id(self, user_id: UUID, tenant_id: UUID) -> User | None:
        statement = select(User).where(
            User.id == user_id,
            User.tenant_id == tenant_id
        )
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()

    # ---------------- CHECK USER EXISTS ----------------
    async def user_exists(self, email: str) -> bool:
        user = await self.get_user_by_email(email)
        return user is not None

    # ---------------- CREATE USER ----------------
    async def create_user(self, user_data: UserCreate) -> User:
        if await self.user_exists(user_data.email):
            raise HTTPException(status_code=400, detail="Email already exists")

        hashed_password = generate_password_hash(user_data.password)

        new_user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password,
            tenant_id=user_data.tenant_id,
        )

        self.db.add(new_user)
        try:
            await self.db.commit()
        except:
            await self.db.rollback()
            raise
        await self.db.refresh(new_user)
        return new_user

    # ---------------- AUTHENTICATE USER ----------------
    async def authenticate_user(self, email: str, password: str) -> User | None:
        user = await self.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    # ---------------- GET ALL USERS (tenant-scoped) ----------------
    async def get_all_users(self, tenant_id: UUID):
        statement = select(User).where(User.tenant_id == tenant_id)
        result = await self.db.execute(statement)
        return result.scalars().all()

    # ---------------- UPDATE USER (normal user) ----------------
    async def update_user(self, user_id: UUID, tenant_id: UUID, user_data: UserUpdate) -> User:
        user = await self.get_user_by_id(user_id, tenant_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        update_data = user_data.model_dump(exclude_unset=True)

        # Hash password if updating
        if "password" in update_data and update_data["password"] is not None:
            update_data["password_hash"] = generate_password_hash(update_data.pop("password"))

        for key, value in update_data.items():
            setattr(user, key, value)

        try:
            await self.db.commit()
        except:
            await self.db.rollback()
            raise
        await self.db.refresh(user)
        return user

    # ---------------- ADMIN UPDATE USER ----------------
    async def admin_update_user(self, user_id: UUID, tenant_id: UUID, user_data: AdminUserUpdate) -> User:
        user = await self.get_user_by_id(user_id, tenant_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        update_data = user_data.model_dump(exclude_unset=True)

        # Hash password if provided
        if "password" in update_data and update_data["password"] is not None:
            update_data["password_hash"] = generate_password_hash(update_data.pop("password"))

        for key, value in update_data.items():
            setattr(user, key, value)

        try:
            await self.db.commit()
        except:
            await self.db.rollback()
            raise
        await self.db.refresh(user)
        return user

    # ---------------- DELETE USER (soft delete) ----------------
    async def delete_user(self, user_id: UUID, tenant_id: UUID):
        user = await self.get_user_by_id(user_id, tenant_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Soft delete: mark inactive
        user.is_active = False

        try:
            await self.db.commit()
        except:
            await self.db.rollback()
            raise
        await self.db.refresh(user)
        return {"message": "User deactivated successfully"}