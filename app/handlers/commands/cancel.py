from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.message import context, message_builder
from app.schemas.user import UserDTO

router = Router()


@router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext, user: UserDTO) -> None:
    await state.clear()

    message_context = context.MainMenu(user.role)
    await message.answer(**message_builder.build(message_context))
