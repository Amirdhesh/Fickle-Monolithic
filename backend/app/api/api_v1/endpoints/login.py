from fastapi import APIRouter,responses,Cookie
from app.schema.user import userCreate
from app.core.db_init import async_session
from sqlalchemy.ext.asyncio.session import AsyncSession
route = APIRouter()



@route.post("/register")
async def create_user(session: async_session):
    ...