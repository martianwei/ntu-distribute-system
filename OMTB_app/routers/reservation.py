from http import HTTPStatus
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from celery import Celery
from pydantic import BaseModel
from exception import LockAcquisitionError, SeatHasReservedError
from configs import configs
from db import session
from db.models.reservation import Reservation, check_seats_can_reserved, create_reservation
from db.models.seat import Seat
from lock.redis import get_lock, release_locks
import logging
from typing import List

logging.basicConfig(level=logging.INFO)


celery_app = Celery(configs.APP_NAME)
celery_app.conf.update(
    broker_url=configs.CELERY_BROKER_URL,
    result_backend=configs.CELERY_RESULT_BACKEND,
)


router = APIRouter()


class reservationRequest(BaseModel):
    user_id: str
    showtime_id: str
    cinema_id: int
    seat_numbers: list[int]


def acquire_locks(showtime_id: int, seat_ids: List[int]):
    locks = []
    try:
        for seat_id in seat_ids:
            lock_key = f"showtime_id={showtime_id} seat_num={seat_id}"
            lock = get_lock(lock_key)
            if lock is None:
                raise LockAcquisitionError(
                    f"Failed to acquire lock for showtime ID: {showtime_id} seat ID: {seat_id}")
            locks.append(lock)
    except LockAcquisitionError:
        release_locks(locks)
        raise
    return locks


def send_reservation_task(reservation_id: int, seat_ids: List[int]):
    return celery_app.send_task(
        "reservation_app.tasks.reservation",
        queue="movie_reservation_queue",
        args=[reservation_id, seat_ids],
    )


@router.post("/reservation", tags=["reservation"])
async def reserve(request: reservationRequest):
    seats = session.query(Seat).filter(
        Seat.cinema_id == request.cinema_id, Seat.seat_number.in_(request.seat_numbers)).all()
    seat_ids = [seat.id for seat in seats]

    try:
        can_reserve = check_seats_can_reserved(
            request.showtime_id, seat_ids)
        if not can_reserve:
            raise SeatHasReservedError(
                f"Seat has been reserved for showtime ID: {request.showtime_id}")
        locks = acquire_locks(request.showtime_id, seat_ids)
        reservation = create_reservation(request.showtime_id, request.user_id)
        task = send_reservation_task(reservation.id, seat_ids)
        return JSONResponse(
            content={"msg": "reserve request success", "taskid": str(task.id)},
            status_code=HTTPStatus.OK,
        )
    except SeatHasReservedError:
        return JSONResponse(
            content={"msg": "the seat have been reserved!!!"},
            status_code=HTTPStatus.BAD_REQUEST,
        )
