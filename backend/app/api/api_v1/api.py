from fastapi import APIRouter
from app.api.api_v1.endpoints.user import route as user_route

api = APIRouter(prefix="/v1.0.0")


api.include_router(user_route, prefix="/user", tags=["USERS"])
