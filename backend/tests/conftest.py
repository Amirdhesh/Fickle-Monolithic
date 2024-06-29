import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from main import app
from sqlmodel import SQLModel
from app.core.settings import settings
from app.core.db_init import get_async_session
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker

async_engine: AsyncEngine = create_async_engine(settings.TEST_DB_URI)


@pytest_asyncio.fixture(scope="session")
async def override_get_async_session():
    async_session = async_sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        yield session
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    await async_engine.dispose()


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client
