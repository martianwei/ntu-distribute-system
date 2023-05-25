from fastapi import APIRouter
from db import session
from db.models.reservation import Reservation
router = APIRouter()

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

