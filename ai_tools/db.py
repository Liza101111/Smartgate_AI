import os
import mariadb
from dotenv import load_dotenv

load_dotenv("/home/sct/smartgate/config.env")


def get_connection():
    return mariadb.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME"),
    )
