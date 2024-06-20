from typing import Annotated
from fastapi import APIRouter, Cookie, HTTPException
from app.core.security import user_credentials
from app.core.db_init import async_session
from app.schema.problemstatement import (
    problemstatementCreate,
    message,
    problemstatementEdit,
    problemstatementRead,
)
from app.crud.problemstatment import (
    add_problemstatement_to_wishlist,
    display_wishlist,
    delete_wishlist,
)

route = APIRouter()


@route.post("/{problemstatement_id}/add_to_wishlist", status_code=200)
async def add_to_wishlist(
    *,
    session: async_session,
    problemstatement_id: str,
    fickel_token: Annotated[str | None, Cookie()] = None
):
    data = await user_credentials(token=fickel_token)
    await add_problemstatement_to_wishlist(
        session=session, problemstatement_id=problemstatement_id, user_id=data.id
    )
    return message(message="Added to wishlist.")


@route.delete("/{problemstatement_id}/remove_from_wishlist", status_code=204)
async def remove_from_wishlist(
    *,
    session: async_session,
    problemstatement_id: str,
    fickel_token: Annotated[str | None, Cookie()] = None
):
    data = await user_credentials(token=fickel_token)
    await delete_wishlist(
        session=session, problemstatement_id=problemstatement_id, user_id=data.id
    )
    return message(message="Removed from wishlist.")


@route.get("/display_wishlist", status_code=200)
async def wishlist_display(
    *, session: async_session, fickel_token: Annotated[str | None, Cookie()] = None
):
    data = await user_credentials(token=fickel_token)
    wishlist = await display_wishlist(session=session, user_id=data.id)
    return wishlist
