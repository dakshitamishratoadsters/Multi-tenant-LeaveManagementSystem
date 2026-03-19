from src.db.session import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db():
    async with SessionLocal() as db:
        yield db