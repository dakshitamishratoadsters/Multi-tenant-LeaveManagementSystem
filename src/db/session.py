from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://tenant:1234@localhost:5432/multitenant"

engine = create_async_engine(
    DATABASE_URL,
    echo=True  # logs SQL queries 
)


SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,  
    expire_on_commit=False
)