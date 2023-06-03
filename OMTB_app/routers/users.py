from fastapi import APIRouter
from db import session
from db.models.reservation import Reservation
from db.models.user import create_user, User
from pydantic import BaseModel

router = APIRouter()

class PostUser(BaseModel):
    id: str
    email: str


# TODO
@router.get("/users/reservation", tags=["users"])
async def get_reservation(user_id: int) -> dict:
    reservations = session.query(Reservation).filter_by(user_id=user_id).all()
    return {
        "reservations": [
            {
                "title": "aqua",
                "movie_starttime": "some datetime",
            }  for reservation in reservations
        ]
    }

@router.get("/user")
async def user_id(id: str):
    existing_user = session.query(User).filter(
        User.username == id
    ).all()
    
    if len(existing_user) == 0:
        return {"user_id": "None"} 
        
    return { "user_id": existing_user[0].id}
     

@router.post("/create_user")
async def create(post_user: PostUser):
    print(post_user.email)
    print(post_user.id)
    try:
        user = User(
            username=post_user.id,
            password="testpassword",
            email=post_user.email,
            activated=True,
        )
        create_user(session, user)
        return {"message": "Create user successfully"}
    except:
        return {"message": "Something went wrong"}

