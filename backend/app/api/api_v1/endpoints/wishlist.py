from typing import Annotated, List
from fastapi import APIRouter, Cookie, Depends
from fastapi_limiter.depends import RateLimiter
from app.core.security import user_credentials
from app.core.db_init import async_session
from app.schema.problemstatement import message, problemstatementwishlist
from fastapi_pagination import Page, paginate
from app.crud.problemstatment import (
    add_problemstatement_to_wishlist,
    display_wishlist,
    delete_wishlist,
)

route = APIRouter()


@route.post("/{problemstatement_id}/add_to_wishlist", status_code=200,dependencies=[Depends(RateLimiter(times=2,seconds=5))])
async def add_to_wishlist(
    *,
    session: async_session,
    problemstatement_id: str,
    fickel_token: Annotated[str | None, Cookie()] = None,
):
    data = await user_credentials(token=fickel_token)
    await add_problemstatement_to_wishlist(
        session=session, problemstatement_id=problemstatement_id, user_id=data.id
    )
    return message(message="Added to wishlist.")


@route.delete("/{problemstatement_id}/remove_from_wishlist", status_code=204,dependencies=[Depends(RateLimiter(times=2,seconds=5))])
async def remove_from_wishlist(
    *,
    session: async_session,
    problemstatement_id: str,
    fickel_token: Annotated[str | None, Cookie()] = None,
):
    data = await user_credentials(token=fickel_token)
    await delete_wishlist(
        session=session, problemstatement_id=problemstatement_id, user_id=data.id
    )
    return message(message="Removed from wishlist.")


@route.get(
    "/display_wishlist", status_code=200, response_model=Page[problemstatementwishlist],dependencies=[Depends(RateLimiter(times=2,seconds=5))]
)
async def wishlist_display(
    *, session: async_session, fickel_token: Annotated[str | None, Cookie()] = None
):
    data = await user_credentials(token=fickel_token)
    wishlist = await display_wishlist(session=session, user_id=data.id)
    return paginate(wishlist)
