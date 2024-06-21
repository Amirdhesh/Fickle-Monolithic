from typing import Annotated
from fastapi import Cookie, APIRouter, Response, HTTPException
from app.schema.user import userCreate, message
from app.core.db_init import async_session, redis_connection
from app.schema.user import (
    userCreate,
    userRead,
    changePassword,
)
from app.crud.user import add_user, change_password, verifyemail
from app.core.security import create_token, user_credentials, email_token
from app.core.settings import settings
from app.celery_worker import send_email_verification
from fastapi.responses import RedirectResponse, HTMLResponse
from pathlib import Path

route = APIRouter()


@route.post("/register", status_code=201, response_model=message)
async def create_user(session: async_session, user_in: userCreate, response: Response):
    user: userRead = await add_user(session=session, user_create=user_in)
    token = await create_token(id=user.id, email=user.email)
    verification_token = await email_token(email=user_in.email)
    send_email_verification.delay(user_in.email, verification_token)
    response.set_cookie(
        key="fickel_token", value=token, expires=(settings.JWT_EXPIRY_TIME * 3600)
    )
    return message(message="User has been successfully added.")


@route.get("/verify-email")
async def verify_email(*, session: async_session, token: str, email: str):
    try:
        r_token = await redis_connection.get(f"{email}_token")
        if r_token == token:
            await verifyemail(session=session, email=email)
            return RedirectResponse(
                url="http://localhost:8000/v1.0.0/user/verification-successfull"
            )
        raise Exception("Token expired")
    except Exception:
        return RedirectResponse(
            url="http://localhost:8000/v1.0.0/user/verification-failed"
        )


@route.get("/verification-successfull", response_class=HTMLResponse)
async def verification_success():
    path = Path(
        r"D:\Projects\Fickel\Monolithic\backend\app\template\verificationsuccess.html"
    )
    with open(path, "r") as file:
        html_file = file.read()
    return html_file


@route.get("/verification-failed", response_class=HTMLResponse)
async def verification_failed():
    path = Path(
        r"D:\Projects\Fickel\Monolithic\backend\app\template\verficationfailed.html"
    )
    with open(path, "r") as file:
        html_file = file.read()
    return html_file


@route.patch("/change_password", status_code=204)
async def Password_change(
    session: async_session,
    password: changePassword,
    fickel_token: Annotated[str | None, Cookie()] = None,
):
    data = await user_credentials(token=fickel_token)
    if password.new_password != password.reenter_password:
        raise HTTPException(status_code=400, detail="Both are different passwords.")
    await change_password(session=session, password=password, id=data.id)
    return message(message="User updated successfully.")


@route.get("/profile")
async def profile_user(*, session: async_session, token: str):
    ...
    """Display user details along with problem posted by that user"""
