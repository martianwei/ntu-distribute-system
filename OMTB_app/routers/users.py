from fastapi import APIRouter

router = APIRouter()


@router.get("/users/sign_in", tags=["users"])
async def sign_in():
    return {"message": "sign_in"}


@router.get("/users/sign_up", tags=["users"])
async def sign_up():
    return {"message": "sign_up"}
