from http import HTTPStatus
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from celery import Celery
from pydatic import BaseModel
from exception import LockAcquisitionError
from configs import configs
from db import session
from db.models.reservation import Reservation
from lock.redis import get_lock, release_locks
celery_app = Celery(configs.APP_NAME)
celery_app.conf.update(
    broker_url=configs.CELERY_BROKER_URL,  # broker，注意rabbitMQ的VHOST要给你使用的用户加权限
    result_backend=configs.CELERY_RESULT_BACKEND,  # backend配置，注意指定redis数据库
)


router = APIRouter()


class reservationRequest(BaseModel):
    user_id: str
    showtime_id: str
    seat_ids: list[int]


@router.post("/main_page/reserve", tags=["main_page"])
async def reserve(request: reservationRequest):
    locks = []
    try:
        # Acquire locks for each seat ID
        for seat_id in request.seat_ids:
            lock_key = f"showtime_id:{request.showtime_id} seat_id:{seat_id}"
            lock = get_lock(lock_key)
            if lock is None:
                raise LockAcquisitionError(
                    f"Failed to acquire lock for showtime ID: {request.showtime_id} seat ID: {seat_id}")
            locks.append(lock)

    except LockAcquisitionError:
        # Release all acquired locks if any lock acquisition fails
        release_locks(locks)
        raise

    # Create a new reservation instance
    reservation = Reservation(
        showtime_id=request.showtime_id,
        user_id=request.user_id,
        status='PENDING'
    )

    # Add the reservation to the session
    session.add(reservation)

    # Commit the session to persist the changes to the database
    session.commit()

    task_id = celery_app.send_task(
        "reservation.task",
        args=[reservation.id, request.seat_ids],
    )

    return JSONResponse(
        content={"msg": "reserve success", "taskid": task_id},
        status_code=HTTPStatus.OK,
    )
