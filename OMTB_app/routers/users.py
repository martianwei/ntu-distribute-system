from fastapi import APIRouter
from db import session
from db.models.reservation import Reservation
from db.models.user import create_user, User
from pydantic import BaseModel

router = APIRouter()
