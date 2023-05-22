from fastapi import FastAPI
from routers import users, login, main_page
import os 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

app = FastAPI()

app.include_router(users.router)
app.include_router(main_page.router)
app.include_router(login.router)


@app.get("/")
async def root() -> dict:
    return {"msg": "Hello root"}


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8888)
