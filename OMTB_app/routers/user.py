from fastapi import APIRouter
from typing import Dict
from db import session
from db.models.reservation import ReservationSchema, get_reservation_by_user_id
router = APIRouter()


@router.get("/user/reservations", tags=["user"])
async def get_reservation(user_id: int) -> Dict[str, list[ReservationSchema]]:
    reservations = get_reservation_by_user_id(user_id)
    # print(reservations)
    # return {"reservations": "good"}
    return {"reservations": reservations}
# -> Dict[str, ReservationSchema]
