from pydantic import BaseModel , EmailStr
from typing import Optional
import uuid

class UserCreate(BaseModel):
    first_name:str
    last_name:str
    username:str
    email:EmailStr
    password:str
    role:str
    tenant_id:uuid.UUID

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class UserUpdate(BaseModel):
    username:str
    email:Optional[EmailStr] = None
    password: Optional[str]=None
    role:Optional[str]=None

class UserResponse(BaseModel):
    id:int
    email:EmailStr
    role:str
    tenant_id:uuid.UUID

    class Config:
        from_attributes = True
        