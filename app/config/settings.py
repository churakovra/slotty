import os
from os import getenv

from aio_pika import ExchangeType
from dotenv import load_dotenv

APP_VERSION = getenv("APP_VERSION") or "dev"


conf_dir = os.path.dirname(__file__)
envs_path = os.path.join(conf_dir, "envs", f"{APP_VERSION}.env")

load_dotenv(envs_path)

BOT_TOKEN = getenv("BOT_TOKEN")

# database
DB_NAME = getenv("DB_NAME")
DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")

# rabbitmq
AMQP_USER = getenv("AMQP_USER")
AMQP_PASSWORD = getenv("AMQP_PASSWORD")
AMQP_HOST = getenv("AMQP_HOST")
AMQP_PORT = getenv("AMQP_PORT")
AMQP_VHOST = getenv("AMQP_VHOST")
AMQP_URL = f"amqp://{AMQP_USER}:{AMQP_PASSWORD}@{AMQP_HOST}/{AMQP_VHOST}"
AMQP_DEFAULT_EXCHANGE = "slotty"
AMQP_DEFAULT_EXCHANGE_TYPE = ExchangeType.DIRECT
AMQP_DEFAULT_QUEUE = "slotty_messages"
AMQP_DEFAULT_ROUTING_KEY = "slotty_message"
