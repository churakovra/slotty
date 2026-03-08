from dataclasses import dataclass

from aiogram.types import InlineKeyboardMarkup


@dataclass
class BotMessage:
    text: str
    reply_markup: InlineKeyboardMarkup | None = None
    parse_mode: str | None = None
