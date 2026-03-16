from dataclasses import dataclass, field

from app.keyboard.markup import BotMarkup


@dataclass
class BotMessage:
    text: str
    markup: BotMarkup | None = field(default=None)
    parse_mode: str | None = field(default=None)
