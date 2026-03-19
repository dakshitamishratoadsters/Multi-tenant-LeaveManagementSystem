from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

 
# Replace with your PostgreSQL credentials
DATABASE_URL = "postgresql+asyncpg://tenant:1234@localhost:5432/multitenant"

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create async session factory
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)