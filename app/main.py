import asyncio

from aiogram import Bot, Dispatcher

from app.config.settings import BOT_TOKEN
from app.handlers import register_routers
from app.middlewares import register_middlewares
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

bot = Bot(BOT_TOKEN)
logger.info("Setup Bot")

async def main():

    dp = Dispatcher()
    register_middlewares(dp)
    register_routers(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
