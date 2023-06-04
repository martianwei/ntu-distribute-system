from fastapi import APIRouter
from typing import Dict
from db.models.reservation import ReservationSchema, get_reservation_by_user_id
from db.models.user import create_user, get_user_by_username, UserSchema
from pydantic import BaseModel
router = APIRouter()


class PostUser(BaseModel):
    username: str
    email: str


@router.get("/user/reservations", tags=["user"])
async def get_reservation(user_id: int) -> Dict[str, list[ReservationSchema]]:
    reservations = get_reservation_by_user_id(user_id)
    return {"reservations": reservations}


@router.post("/user", tags=["user"])
async def create(post_user: PostUser):
    print(post_user.email)
    print(post_user.username)
    try:
        user = UserSchema(
            username=post_user.username,
            password="testpassword",
            email=post_user.email,
            activated=True,
        )
        create_user(user)

        return {"message": "Create user successfully"}
    except:
        return {"message": "Something went wrong"}


@router.get("/user", tags=["user"])
async def get_user_request(username):
    user = get_user_by_username(str(username))

    if user is None:
        return {"user_id": "None"}

    return {"user_id": user.id}
