from fastapi import APIRouter
from app.api.api_v1.endpoints.login import route as login_route
from app.api.api_v1.endpoints.user import route as user_route
from app.api.api_v1.endpoints.problemstatement import route as problemstatment_route
from app.api.api_v1.endpoints.solution import route as solution_route
from app.api.api_v1.endpoints.wishlist import route as wishlist_route

api = APIRouter(prefix="/v1.0.0")

api.include_router(login_route, tags=["LOGIN"])
api.include_router(user_route, prefix="/user", tags=["USERS"])
api.include_router(
    problemstatment_route, prefix="/problemstatement", tags=["PROBLEM STATEMENT"]
)
api.include_router(solution_route, prefix="/solution", tags=["SOLUTION"])
api.include_router(wishlist_route, prefix="/wishlist", tags=["WISHLIST"])
