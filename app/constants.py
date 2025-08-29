import os
from helpers.aws.secrets_manager import get_secret

ENV = os.getenv("ENV", "local")

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

if ENV != "local":
    SM_SERASA_SERVICE_DATABASE = os.getenv("SM_SERASA_SERVICE_DATABASE")
    response = get_secret(SM_SERASA_SERVICE_DATABASE)

    POSTGRES_HOST = response["HOST"]
    POSTGRES_DB = response["DATABASE"]
    POSTGRES_USER = response["USER"]
    POSTGRES_PASSWORD = response["PASSWORD"]


DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"
