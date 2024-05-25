import jwt
import bcrypt
import secrets
from fastapi import HTTPException
from datetime import timedelta, datetime
from pytz import timezone
from uuid import UUID
from app.core.settings import settings
from app.core.db_init import redis_connection
from app.schema.user import TokenResponse
from uuid import UUID

def hash_password(password: str):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode('utf-8')


def check_pw(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode('utf-8'))


async def create_token(id: UUID, email: str):
    ist = timezone("Asia/Kolkata")
    expiry = datetime.now(ist) + timedelta(hours=settings.JWT_EXPIRY_TIME)
    payload = {"id": str(id), "email": email, "exp": expiry.timestamp()}
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM) #problem
    await redis_connection.setex(
        name = f'access_token_{id}',
        value = token,
        time = settings.JWT_EXPIRY_TIME * 3600
    )
    return token


async def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
        return payload
    except:
        return None


async def user_credentials(token: str):
    try :
        data =await decode_token(token=token)
        if not data:
            raise ValueError("Invalid Token 1")
        redis_token = await redis_connection.get(f"access_token_{data['id']}")
        if redis_token:
            if redis_token == token:
                return TokenResponse(id = UUID(data["id"]),email=data["email"])
            raise ValueError("Invalid Token 2")
        raise ValueError("Invalid Token 3")
    except Exception as e:
        raise HTTPException(status_code=401,detail=f'{e}')
    

async def email_token(email: str):
    token = secrets.token_urlsafe(16)
    await redis_connection.setex(
        name=f"{email}_token",
        value=str(token),
        time=5*60
    )
    return str(token)
