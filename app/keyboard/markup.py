from dataclasses import dataclass


@dataclass
class MarkupButton:
    text: str
    callback: str


@dataclass
class BotMarkup:
    rows: list[list[MarkupButton]]
