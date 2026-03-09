import os
from os import getenv

from dotenv import load_dotenv

APP_VERSION = getenv("APP_VERSION") or "dev"


conf_dir = os.path.dirname(__file__)
envs_path = os.path.join(conf_dir, "envs", f"{APP_VERSION}.env")

load_dotenv(envs_path)

BOT_TOKEN = getenv("BOT_TOKEN")

DB_NAME = getenv("DB_NAME")
DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
