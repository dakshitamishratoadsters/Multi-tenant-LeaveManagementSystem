from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.models.user_model import User
from src.core.security import hash_password
import uuid

class UserService:
    def __init__(self, db:AsyncSession):
        self.db = db

    async def create_user(self, user):
        hashed_password = hash_password(user.password)

        new_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            email=user.email,
            password=hashed_password,
            role=user.role,
            tenant_id=user.tenant_id
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)

        return new_user



    async def get_all_users(self, tenant_id: uuid.UUID):
        result = await self.db.execute(
            select(User).where(User.tenant_id == tenant_id)
        )
        return result.scalars().all()
    

    async def get_user_by_id(self, user_id:int, tenant_id: uuid.UUID):
        result = await self.db.execute(
            select(User).where(
                User.id == user_id,
                User.tenant_id == tenant_id
            )
        )
        return result.scalars().first()
    

    async def update_user(self, user_id:int, updated_data, tenant_id:uuid.UUID):
        user = await self.get_user_by_id(user_id, tenant_id)

        if not user:
            return None
        
        for field, value in updated_data.model_dump(exclude_unset=True).items():
            if hasattr(user, field) and value is not None:
                setattr(user, field, value)

        await self.db.commit()
        await self.db.refresh(user)

        return user
    

    async def delete_user(self, user_id:int, tenant_id:uuid.UUID):
        user = await self.get_user_by_id(user_id, tenant_id)

        if not user:
            return None
        
        await self.db.delete(user)
        await self.db.commit()

        return {"message": "User deleted successfully"}
    

    