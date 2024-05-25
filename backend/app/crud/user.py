from app.model import Users
from fastapi import HTTPException
from redis.asyncio import Redis
from sqlalchemy.orm import selectinload
from sqlmodel import select
from fastapi.responses import RedirectResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.security import hash_password,check_pw,create_token
from app.schema.user import userCreate, userLogin, userRead, userUpdate,loginUser,changePassword
from uuid import UUID,uuid4
from app.celery_worker import send_otp_for_forget_password
from app.core.db_init import redis_connection

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
    

async def update_user(*,session: AsyncSession,user_update:userUpdate,id:UUID):
    try:
        user = await session.get(Users,id)
        if not user:
            raise ValueError("User with this id not in the database.")
        user_data = user_update.model_dump(exclude_unset=True)
        user.sqlmodel_update(user_data)
        session.add(user)
        await session.commit()
        await session.refresh()
        return user
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"User not updated '{e}'"
        )
    
    

async def login_user(*,session:AsyncSession,user_login:loginUser):
    try:
        statement = select(Users).where(Users.email == user_login.email)
        user = (await session.exec(statement=statement)).one_or_none()
        if user:
            if check_pw(user_login.password,user.password):
                return await create_token(id=user.id,email=user.email)
            raise ValueError("Invalid password")
        raise ValueError("Invalid Email/Password")
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"{e}"
        )


async def change_password(*,session:AsyncSession,id:UUID,password:changePassword):
    try:
        user = await session.get(Users,id)
        hashed_password = hash_password(password.new_password)
        user.password = hashed_password
        session.add(user)
        await session.commit()
        await session.refresh(user)
    except Exception as e:
        raise HTTPException(
            status_code= 400,
            detail={f"Password not changed. {str(e)}"}
        )
    

async def forget_password_otp(*,session:AsyncSession,email:str):
    try:
        statement = select(Users).where(Users.email == email)
        user = (await session.exec(statement=statement)).one_or_none()
        if not user:
            raise ValueError("Invalid Email")
        otp = str(uuid4().int)[-6:]
        send_otp_for_forget_password.delay(email,otp)
        await redis_connection.setex(
            name=f'forget_password_otp:{email}',
            value=otp,
            time = 600
        )
        return f"OTP has been send to the {email}"
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


async def verifyemail(*,session:AsyncSession, email:str):
    try:
        statement = select(Users).where(Users.email == email)
        user = (await session.exec(statement=statement)).one()
        user.email_verified = True
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return 0
    except Exception as e:
        raise Exception(e)
