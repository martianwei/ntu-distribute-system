from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import user, login, reservation, movie, showtime, seat
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


app.include_router(user.router)
app.include_router(login.router)
app.include_router(reservation.router)
app.include_router(movie.router)
app.include_router(showtime.router)
app.include_router(seat.router)


@app.get("/")
async def root() -> dict:
    return {"msg": "Hello root"}
