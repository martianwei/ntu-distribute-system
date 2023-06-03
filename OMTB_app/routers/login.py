from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, JSONResponse
from oauth.google import flow, authorization_url
from configs import configs
from db.models.user import create_user, UserSchema, get_user_by_username


router = APIRouter()


# for testing in browser
@router.get("/login", response_class=RedirectResponse, tags=["login"])
async def login():
    return authorization_url


@router.post("/login", response_class=RedirectResponse, tags=["login"])
async def login():
    return authorization_url


@router.get("/secret", tags=["login"])
async def secret():
    try:
        auth_session = flow.authorized_session()
        return "you found my secret"
    except:
        return "Don't peak my secret"


@router.get("/callback", tags=["login"])
async def callback(request: Request):
    return RedirectResponse(configs.CLIENT_ENDPOINT)
