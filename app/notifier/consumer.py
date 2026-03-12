import aio_pika

from app.config.settings import (
        AMQP_URL,
        AMQP_DEFAULT_QUEUE, 
        )
from app.utils.logger import setup_logger 

logger = setup_logger(__name__)

class MessageConsumer:
    def __init__(self) -> None:
        self.connection = None
        self.channel = None
        self.queue = None

    async def start(self):
        self.connection = await aio_pika.connect_robust(AMQP_URL)
        self.channel = await self.connection.channel()
        self.queue = await self.channel.declare_queue(AMQP_DEFAULT_QUEUE) 
        logger.info("MessageConsumer been started")

    async def stop(self):
        if self.channel:
            await self.channel.close()
        if self.connection:
            await self.connection.close()

