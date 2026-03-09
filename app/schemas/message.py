from aiogram.types import InlineKeyboardMarkup
from pydantic import BaseModel


class BotMessage(BaseModel):
    text: str
    reply_markup: InlineKeyboardMarkup | None
    parse_mode: str | None
