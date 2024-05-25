from fastapi import APIRouter
from app.api.api_v1.endpoints.login import route as login_route
from app.api.api_v1.endpoints.user import route as user_route

api = APIRouter(prefix="/v1.0.0")

api.include_router(login_route,tags=["LOGIN"])
api.include_router(user_route, prefix="/user", tags=["USERS"])
