import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME: str = os.getenv("APP_NAME")
POSTGRES_URL: str = os.getenv("POSTGRES_URL")

CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND")

REDIS_LOCK_URL: str = os.getenv("REDIS_LOCK_URL")


GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET")
SERVER_PORT: str = os.getenv("SERVER_PORT")
SECRET_KEY: str = os.getenv("SECRET_KEY")