from fastapi import APIRouter
from typing import Dict
from db import session
from db.models.reservation import ReservationSchema, get_reservation_by_user_id
router = APIRouter()


@router.get("/users/reservations", tags=["user"])
async def get_reservation(user_id: int) -> Dict[str, ReservationSchema]:
    reservations = get_reservation_by_user_id(user_id)
    return {"reservations": reservations}
