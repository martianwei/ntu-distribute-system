from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, JSONResponse
from oauth.google import flow, authorization_url
from configs import configs
from db.models.user import create_user, UserSchema, get_user_by_username

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
        token = flow.fetch_token(
            authorization_response=str(authorization_response))
        # print(token)
        auth_session = flow.authorized_session()
        data = auth_session.get(
            'https://www.googleapis.com/userinfo/v2/me').json()
        print(data)
        user = get_user_by_username(data['id'])

        if user is None:
            print("Creating new user")
            new_user = UserSchema(
                username=str(data['id']),
                password="testpassword",
                email=data['email'],
                activated=True,
            )
            user = create_user(new_user)

        return {
            "user_id": user.id
        }
    except:
        return "Auth failed!"
