import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME: str = os.getenv("APP_NAME")
print(f"=================={APP_NAME}==================")


# postgres 設定
POSTGRES_HOSTNAME: str = os.getenv('POSTGRES_HOSTNAME')
POSTGRES_PORT: int = int(os.getenv('POSTGRES_PORT'))
POSTGRES_USER: str = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB: str = os.getenv('POSTGRES_DB')


# rabbitmq 設定
RABBITMQ_HOSTNAME: str = os.getenv('RABBITMQ_HOSTNAME')
RABBITMQ_PORT: int = int(os.getenv('RABBITMQ_PORT'))
RABBITMQ_USERNAME: str = os.getenv('RABBITMQ_USERNAME')
RABBITMQ_PASSWORD: str = os.getenv('RABBITMQ_PASSWORD')
RABBITMQ_VHOST: str = os.getenv('RABBITMQ_VHOST')


# redis 設定
REDIS_HOSTNAME: str = os.getenv('REDIS_HOSTNAME')
REDIS_PORT: int = os.getenv('REDIS_PORT')
REDIS_PASSWORD: str = os.getenv('REDIS_PASSWORD')
REDIS_TASK_DB: int = os.getenv('REDIS_TASK_DB')
REDIS_LOCK_DB: int = os.getenv('REDIS_LOCK_DB')


CELERY_BROKER_URL = f"amqp://{RABBITMQ_USERNAME}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOSTNAME}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}"
CELERY_RESULT_BACKEND = f"redis://:{REDIS_PASSWORD}@{REDIS_HOSTNAME}:{REDIS_PORT}/{REDIS_TASK_DB}"
POSTGRES_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOSTNAME}:{POSTGRES_PORT}/{POSTGRES_DB}"
REDIS_LOCK_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOSTNAME}:{REDIS_PORT}/{REDIS_LOCK_DB}"


SERVER_PORT: str = os.getenv("SERVER_PORT")
CLIENT_ENDPOINT: str = os.getenv("CLIENT_ENDPOINT")
