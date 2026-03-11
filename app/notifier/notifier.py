import asyncio

from aiogram import Bot


class Notifier:
    def __init__(self, bot: Bot):
        self.bot = Bot

    async def send_message(self, bot_message, receivers):
        tasks = []
        for receiver in receivers:
            tasks.append(
                asyncio.Task(self.bot.send_message(chat_id=receiver.id, **bot_message))
            )
        asyncio.gather(*tasks)
