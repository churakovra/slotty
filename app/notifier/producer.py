import aio_pika

from app.config.settings import AMQP_URL


class NotifyProducer:
    def __init__(self):
        self.connection = aio_pika.connect_robust(AMQP_URL)


    async def produce(self):
        pass