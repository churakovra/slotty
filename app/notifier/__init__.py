import asyncio

from app.notifier.consumer import MessageConsumer
from app.notifier.notifier import Notifier


async def setup_consumer(bot) -> None:
    notifier = Notifier(bot)
    consumer = MessageConsumer(notifier)
    await consumer.start()
    try:
        await asyncio.Future()
    finally:
        await consumer.stop()
