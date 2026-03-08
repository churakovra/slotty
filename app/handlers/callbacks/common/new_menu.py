from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.keyboard.callback_factories.menu import MenuCallback
from app.message import context, message_builder
from app.schemas.user import UserDTO
from app.utils.enums.menu_type import MenuType

router = Router()


@router.callback_query(MenuCallback.filter(F.menu_type == MenuType.NEW))
async def handle_callback(
    callback: CallbackQuery, callback_data: MenuCallback, user: UserDTO
):
    message_context = context.MainMenu(user.role)
    await callback.message.answer(**message_builder.build(message_context))
    await callback.answer()
