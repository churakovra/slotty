from typing import Any

from app.keyboard import markup_builder
from app.message.context import AbstractBotMessageContext
from app.schemas.message import BotMessage


class BotMessageBuilder:
    def build(self, context: AbstractBotMessageContext) -> dict[str, Any]:
        text = context.text
        markup = markup_builder.build(context.markup_context) if context.markup_context else None
        return BotMessage(text=text, reply_markup=markup, parse_mode=context.parse_mode).model_dump()


message_builder = BotMessageBuilder()