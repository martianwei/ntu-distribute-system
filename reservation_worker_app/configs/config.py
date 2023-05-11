import os
from dotenv import load_dotenv

load_dotenv()


POSTGRESQL_URL = os.getenv("POSTGRESQL_URL")
POSTGRESQL_DB_NAME = os.getenv("POSTGRESQL_DB_NAME")
POSTGRESQL_DB_USER = os.getenv("POSTGRESQL_DB_USER")
POSTGRESQL_DB_PASSWORD = os.getenv("POSTGRESQL_DB_PASSWORD")
