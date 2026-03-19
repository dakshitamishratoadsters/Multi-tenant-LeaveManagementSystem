from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List
import uuid

from src.db.models.tenant_model import Tenant
from src.schemas.tenant_schema import TenantCreate, TenantUpdate


class TenantServices:

    def __init__(self, db: AsyncSession):
        self.db = db

    # ======================= CREATE =======================
    async def create_tenant(self, tenant_data: TenantCreate) -> Tenant:
        try:
            # Check domain uniquenes
            if tenant_data.domain:
                result = await self.db.execute(
                    select(Tenant).where(Tenant.domain == tenant_data.domain)
                )
                existing = result.scalar_one_or_none()

                if existing:
                    raise ValueError("Domain already exists")

            # 🎟️ Generate invite code
            invite_code = getattr(tenant_data, "invite_code", None) or str(uuid.uuid4())[:8]

            
            tenant = Tenant(
                name=tenant_data.name,
                company_size=tenant_data.company_size,
                company_type=tenant_data.company_type,
                domain=tenant_data.domain,
                invite_code=invite_code,
               )

            self.db.add(tenant)
            await self.db.commit()
            await self.db.refresh(tenant)

            return tenant

        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e

    # ======================= GET ONE =======================
    async def get_tenant(self, tenant_id: uuid.UUID) -> Optional[Tenant]:
        result = await self.db.execute(
            select(Tenant).where(Tenant.id == tenant_id)
        )
        return result.scalar_one_or_none()

    # ======================= GET ALL =======================
    async def get_all_tenants(self) -> List[Tenant]:
        result = await self.db.execute(select(Tenant))
        return result.scalars().all()

    # ======================= UPDATE =======================
    async def update_tenant(
        self,
        tenant_id: uuid.UUID,
        tenant_data: TenantUpdate
    ) -> Optional[Tenant]:

        tenant = await self.get_tenant(tenant_id)

        if not tenant:
            return None

        # Only update provided fields
        update_data = tenant_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(tenant, key, value)

        try:
            self.db.add(tenant)
            await self.db.commit()
            await self.db.refresh(tenant)
            return tenant

        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e

    # ======================= DELETE =======================
    async def delete_tenant(self, tenant_id: uuid.UUID) -> bool:
        tenant = await self.get_tenant(tenant_id)

        if not tenant:
            return False

        try:
            await self.db.delete(tenant)
            await self.db.commit()
            return True

        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e