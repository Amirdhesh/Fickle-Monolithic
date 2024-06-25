from fastapi import APIRouter, Response
from app.core.db_init import async_session, redis_connection
from app.core.settings import settings
from app.core.security import user_credentials
from app.schema.user import loginUser, message
from app.crud.user import login_user, forget_password_otp

route = APIRouter()


@route.post("/login", status_code=200, response_model=message)
async def login_users(
    *, session: async_session, login_detail: loginUser, response: Response
):
    token = await login_user(session=session, user_login=login_detail)
    response.set_cookie(
        key="fickel_token", value=token, expires=(settings.JWT_EXPIRY_TIME * 3600)
    )
    return message(
        message=f"Login successfull👍",
    )


@route.delete("/logout", status_code=204)
async def logout_user(*, response: Response, token: str):
    response.delete_cookie("fickel_token")
    data = await user_credentials(token)
    await redis_connection.delete(f"access_token_{data.id}")
    return message(message="Logout successfull👍.")


@route.get("/forget_password/{emailid}", status_code=204)
async def forget_password(*, session: async_session, email: str):
    return message(message=(await forget_password_otp(session=session, email=email)))
