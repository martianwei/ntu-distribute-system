from fastapi import FastAPI
from routers import users, login, main_page
import os 
from configs import configs
from fastapi.middleware.cors import CORSMiddleware
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

app = FastAPI()

app.include_router(users.router)
app.include_router(main_page.router)
app.include_router(login.router)

origins = [
    configs.CLIENT_ENDPOINT,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root() -> dict:
    return {"msg": "Hello root"}


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8888)
