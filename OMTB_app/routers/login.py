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

# Test for OAuth session
@router.get("/secret")
async def secret():
    try:
        auth_session = flow.authorized_session()
        return "you found my secret"
    except:
        return "Don't peak my secret"


@router.get("/callback")
async def callback(request: Request):
    try:
        authorization_response = request.url
        token = flow.fetch_token(authorization_response=str(authorization_response))
        # print(token)
        auth_session = flow.authorized_session()
        data = auth_session.get('https://www.googleapis.com/userinfo/v2/me').json()

        existing_user = session.query(User).filter(
            User.username == data['id']
        ).all()
        
        # No such user, create one
        if len(existing_user) == 0:     
            user = User(
                username=data['id'],
                password="testpassword",
                email=data['email'],
                activated=True,
            )
            create_user(session, user)
            existing_user = session.query(User).filter(
                User.username == data['id']
            ).all()        
        return { "user_id": existing_user[0].id}
    
    except:
        return "Auth failed!"
