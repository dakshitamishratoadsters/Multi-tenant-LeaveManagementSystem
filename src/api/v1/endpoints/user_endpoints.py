from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from src.db.deps import get_db
from src.services.user_services import UserService
from src.schemas.user_schemas import UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
async def get_users(db:AsyncSession = Depends(get_db)):
    service = UserService(db)
    # Using a sample UUID - replace with actual tenant logic
    sample_tenant_id = uuid.UUID("12345678-1234-5678-9abc-123456789abc")
    return await service.get_all_users(tenant_id=sample_tenant_id)

@router.get("/{user_id}")
async def get_user(user_id:int, db:AsyncSession = Depends(get_db)):
    service = UserService(db)
    # Using a sample UUID - replace with actual tenant logic
    sample_tenant_id = uuid.UUID("12345678-1234-5678-9abc-123456789abc")

    user = await service.get_user_by_id(user_id , tenant_id=sample_tenant_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.post("/")
async def create_user(user:UserCreate, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    return await service.create_user(user)

@router.put("/{user_id}")
async def update_user(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    # Using a sample UUID - replace with actual tenant logic
    sample_tenant_id = uuid.UUID("12345678-1234-5678-9abc-123456789abc")

    update_user = await service.update_user(user_id, user, tenant_id=sample_tenant_id)

    if not update_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return update_user

@router.delete("/{user_id}")
async def delete_user(user_id:int, db:AsyncSession = Depends(get_db)):
    service = UserService(db)
    # Using a sample UUID - replace with actual tenant logic
    sample_tenant_id = uuid.UUID("12345678-1234-5678-9abc-123456789abc")

    result = await service.delete_user(user_id, tenant_id=sample_tenant_id)

    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    
    return result


