import asyncio

from aiogram import Bot, Dispatcher

from app.config.settings import BOT_TOKEN
from app.handlers import register_routers
from app.middlewares import register_middlewares
from app.notifier.producer import NotifyProducer
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

bot = bot(bot_token)
logger.info("Start Bot")

async def main():

    message_producer = NotifyProducer()
    await message_producer.start()
    
    dp = Dispatcher()
    register_middlewares(dp)
    register_routers(dp)

    await bot.delete_webhook(drop_pending_updates=True)

    # startup
    await dp.start_polling(bot)

    # utilization
    await message_producer.stop()

if __name__ == "__main__":
    asyncio.run(main())
