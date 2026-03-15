import asyncio

from aiogram import Bot, Dispatcher

from app.config.settings import BOT_TOKEN, SERVICE_TYPE
from app.handlers import register_routers
from app.middlewares import register_middlewares
from app.notifier import setup_consumer
from app.notifier.producer import MessageProducer
from app.utils.enums.common import ServiceType
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

bot = Bot(BOT_TOKEN)
logger.info("Start Bot")


async def main() -> None:

    if SERVICE_TYPE == ServiceType.CONSUMER:
        await setup_consumer(bot)
        return

    message_producer = MessageProducer()
    await message_producer.start()

    dp = Dispatcher(
        producer=message_producer,
    )
    register_middlewares(dp)
    register_routers(dp)

    # startup
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

    # utilization
    await message_producer.stop()


if __name__ == "__main__":
    asyncio.run(main())
