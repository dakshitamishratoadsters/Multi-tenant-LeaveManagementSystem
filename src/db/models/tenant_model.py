from sqlmodel import Column, Relationship, SQLModel, Field
from datetime import datetime
import uuid
import enum
from typing import TYPE_CHECKING, Optional,List
if TYPE_CHECKING:
    from src.db.models.user_model import User
from sqlalchemy import types as pg


class CompanyType(str, enum.Enum):
    IT = "IT/Software"
    FINANCE = "Finance/Banking"
    HEALTHCARE = "Healthcare"
    EDUCATION = "Education"
    ECOMMERCE = "E-commerce"
    MARKETING = "Marketing"
    CONSULTING = "Consulting"
    MANUFACTURING = "Manufacturing"

class CompanySize(str,enum.Enum):
    SMALL = "1-50"
    MEDIUM = "51-200"
    LARGE = "201-1000"
    ENTERPRISE = "1000+"
        


class Tenant(SQLModel, table=True):
    __tablename__ = "tenants"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str =Field(index=True)
    company_type: CompanyType
    company_size: CompanySize
    domain: Optional[str] = Field(default=None, unique=True)
    invite_code: Optional[str] = Field(default=None, unique= True ,index=True)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    )
    users: List["User"] = Relationship(
    back_populates="tenant",
    sa_relationship_kwargs={
        "cascade": "all, delete-orphan",
        "passive_deletes": True
    }
)