from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.keyboard.context import AbstractMarkupContext
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class MarkupBuilder:
    def build(self, context: AbstractMarkupContext) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        fabric = context.fabric
        buttons, adjust = fabric(context)
        for button_text, callback in buttons:
            builder.button(text=button_text, callback_data=callback)
        builder.adjust(adjust)
        return builder.as_markup()


markup_builder = MarkupBuilder()
