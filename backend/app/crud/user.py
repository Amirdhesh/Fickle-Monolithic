from app.model import Users
from fastapi import HTTPException
from redis.asyncio import Redis
from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.security import hash_password
from app.schema.user import userCreate, userLogin, userRead, userUpdate


async def add_user(*, session: AsyncSession, user_create: userCreate):
    try:
        user = Users.model_validate(
            user_create, update={"password": hash_password(user_create.password)}
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    except Exception as e:
        raise HTTPException(status_code=409, detail=f"User already exist. {e}")
