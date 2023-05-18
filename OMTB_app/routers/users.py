from fastapi import APIRouter
from db import session
from db.models.user import create_user, User
router = APIRouter()


@router.get("/users/sign_in", tags=["users"])
async def sign_in():
    return {"message": "sign_in"}


@router.get("/users/sign_up", tags=["users"])
async def sign_up():
    user = User(
        username="test",
        password="testpassword",
        email="test@example.com",
        activated=True,
    )
    create_user(session, user)
    return {"message": "sign_up"}
