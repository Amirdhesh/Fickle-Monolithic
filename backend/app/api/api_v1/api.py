from fastapi import APIRouter
from backend.app.api.api_v1.endpoints.login import route as login_route

api = APIRouter(prefix="v1.0.0")


api.include_router(login_route,prefix="/user",tags=["USERS"])