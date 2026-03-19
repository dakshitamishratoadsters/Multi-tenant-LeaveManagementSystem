from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import ForeignKey
import uuid


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)

    first_name: str
    last_name: str
    username: str = Field(index=True)
    email: str = Field(index=True, unique=True)

    password: str
    role: Optional[str] = None
    is_active: bool = True

    tenant_id: uuid.UUID = Field(foreign_key="tenants.id", sa_column_kwargs={"nullable": False})

    # relationship
    # tenant: Optional["Tenant"] = Relationship(back_populates="users")