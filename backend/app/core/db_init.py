from typing import Annotated
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.settings import settings
from redis.asyncio import Redis
from fastapi import Depends

async_engine: AsyncEngine = create_async_engine(settings.DB_URI)


async def get_async_session() -> AsyncSession:  # type: ignore
    async_session = async_sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session



redis_connection = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,  # used to return decoded ouput from redis
)

async_session = Annotated[AsyncSession, Depends(get_async_session)]
