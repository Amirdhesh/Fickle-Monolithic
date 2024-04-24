from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.core.settings import settings


async_engine : AsyncEngine = create_async_engine(settings.DB_URI)


async def get_async_session() -> AsyncSession:
    async_session = async_sessionmaker(bind=async_engine,class_=AsyncSession,expire_on_commit=False)
    async with async_session() as session:
        yield session

