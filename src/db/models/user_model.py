from typing import Optional, TYPE_CHECKING
from sqlmodel import Column, SQLModel, Field, Relationship
from sqlalchemy import DateTime, ForeignKey
from datetime import datetime
import uuid

if TYPE_CHECKING:
    from src.db.models.tenant_model import Tenant


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    username: str = Field(index=True, unique=True, nullable=False)
    email: str = Field(index=True, unique=True, nullable=False)
    password_hash: str = Field(nullable=False)
    role: str = Field(default="employee",)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
            nullable=False
        )
    )

    tenant_id: uuid.UUID = Field(
        sa_column=Column(
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
)

    tenant: Optional["Tenant"] = Relationship(back_populates="users")