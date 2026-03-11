import json
from typing import Any

import aio_pika

from app.config.settings import (
    AMQP_DEFAULT_EXCHANGE,
    AMQP_DEFAULT_EXCHANGE_TYPE,
    AMQP_DEFAULT_ROUTING_KEY,
    AMQP_URL,
)
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class MessageProducer:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.exchange = None

    async def start(self):
        self.connection = await aio_pika.connect_robust(AMQP_URL)
        self.channel = await self.connection.channel()
        self.exchange = await self.channel.declare_exchange(
            AMQP_DEFAULT_EXCHANGE, AMQP_DEFAULT_EXCHANGE_TYPE
        )
        logger.info("MessageProducer has been started")

    async def produce(self, bot_message: dict[str, Any]):
        body = json.dumps(bot_message).encode("utf-8")
        message = aio_pika.Message(body, content_type="application/json")
        await self.exchange.publish(message, routing_key=AMQP_DEFAULT_ROUTING_KEY)

    async def stop(self):
        if self.channel:
            await self.channel.close()
        if self.connection:
            await self.connection.close()
        logger.info("MessageProducer has been stopped")
