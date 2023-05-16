import os
from dotenv import load_dotenv

load_dotenv()


POSTGRES_URL = os.getenv("POSTGRES_URL")
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
