from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, JSONResponse
from oauth.google import flow, authorization_url
from configs import configs
import jwt

router = APIRouter()


@router.get("/login", response_class=RedirectResponse)
async def login():
    return authorization_url


@router.get("/callback")
async def callback(request: Request):
    authorization_response = request.url
    flow.fetch_token(authorization_response=str(authorization_response))
    session = flow.authorized_session()
    data = session.get('https://www.googleapis.com/userinfo/v2/me').json()

    # return token when authorized
    # key = configs.SECRET_KEY
    # token = jwt.encode({"email": f"{data.email}"}, key, algorithm="HS256")

    # response = JSONResponse(content=data)
    # response.headers["Authorization"] = f"Bearer {token}"
    # Verify token
    # info = jwt.decode(encoded, key, algorithms="HS256")

    return data
