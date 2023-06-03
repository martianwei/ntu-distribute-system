from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, JSONResponse
from oauth.google import flow, authorization_url
from configs import configs
from db import session
from db.models.user import create_user, User


router = APIRouter()


# for testing in browser
@router.get("/login", response_class=RedirectResponse)
async def login():
    return authorization_url

@router.post("/login", response_class=RedirectResponse)
async def login():
    return authorization_url



@router.get("/callback")
async def callback(request: Request):
    return RedirectResponse(configs.CLIENT_ENDPOINT)