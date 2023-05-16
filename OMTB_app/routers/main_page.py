import http
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from celery import Celery
from pydantic import BaseModel
from configs import configs
from db.postgresql import postgresqlClient
celery_app = Celery("OMTB_app")
celery_app.conf.update(
    broker_url=configs.CELERY_BROKER_URL,  # broker，注意rabbitMQ的VHOST要给你使用的用户加权限
    result_backend=configs.CELERY_RESULT_BACKEND,  # backend配置，注意指定redis数据库
)


router = APIRouter()


class reservationRequest(BaseModel):
    user_id: str
    showtime_id: str
    seat_id: list


@router.post("/main_page/reserve", tags=["main_page"])
async def reserve(request: reservationRequest):

    # movie_title = postgresqlClient.cur.execute(
    #     '''
    #         SELECT title
    #         FROM showtimes
    #         INNER JOIN movies ON showtimes.movie_id = movies.id
    #         WHERE showtimes.id = {0}
    #     '''.format(request.showtime_id)
    # )
    postgresqlClient.cur.execute(
        '''
            INSERT INTO reservations (user_id, showtime_id, seat_id, status)
            VALUES ('{0}', '{1}', '{2}', 'pending')
        '''.format(request.user_id, request.showtime_id, request.seat_id)
    )

    taskid = celery_app.send_task(
        "reservation.task",
        args=[request.user_id, request.showtime_id, request.seat_id],
    )
    return JSONResponse(
        content={"code": http.SUCCESS,
                 "message": "register task dispatched", "taskid": taskid},
        status_code=http.SUCCESS,
    )
