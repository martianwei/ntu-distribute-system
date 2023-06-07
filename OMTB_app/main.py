from fastapi import FastAPI
import os
from configs import configs
# from starlette.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
from routers import user, reservation, movie, showtime, seat

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


app.include_router(user.router)
app.include_router(reservation.router)
app.include_router(movie.router)
app.include_router(showtime.router)
app.include_router(seat.router)


@app.get("/")
async def root() -> dict:
    return {"msg": "Hello root"}
