import aio_pika

from app.config.settings import AMQP_DEFAULT_EXCHANGE, AMQP_DEFAULT_EXCHANGE_TYPE, AMQP_URL
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class NotifyProducer:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.exchange = None

    async def start(self):
        self.connection = await aio_pika.connect_robust(AMQP_URL)
        self.channel = await self.connection.channel()
        self.exchange = await self.channel.declare_exchange(AMQP_DEFAULT_EXCHANGE, AMQP_DEFAULT_EXCHANGE_TYPE)
        logger.info("NofityProducer has been started")


    async def produce(self):
        pass


    async def stop(self):
        if self.channel:
            await self.channel.close()
        if self.connection:
            await self.connection.close()
