from sqlmodel import SQLModel ,Field
from datetime import datetime
import uuid
from typing import Optional
from src.db.models.tenant_model import CompanyType,CompanySize
from pydantic import BaseModel

class TenantCreate(BaseModel):
    name:str
    company_size: CompanySize
    company_type: CompanyType
    domain:Optional[str]=None
    invite_code: Optional[str]=None

class TenantRead(BaseModel):
    id:uuid.UUID
    name:str
    company_size:CompanySize
    company_type:CompanyType
    domain:Optional[str]=None
    invite_code:Optional[str]=None 
    created_at:datetime 

    class Config:
        orm_mode=True 

class TenantUpdate(BaseModel):
    name: Optional[str] = None
    company_size: Optional[CompanySize] = None
    company_type: Optional[CompanyType] = None
    domain: Optional[str] = None
    invite_code: Optional[str] = None         
    
