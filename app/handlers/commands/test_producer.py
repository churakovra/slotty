from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.keyboard.context import MainMenuKeyboardContext
from app.message import context
from app.message.message_pack import MessagePack, MessageRecipient
from app.notifier.producer import MessageProducer
from app.utils.enums.bot_values import UserRole
from app.utils.logger import setup_logger

router = Router()
logger = setup_logger(__name__)


@router.message(Command("produce"))
async def produce(message: Message, producer: MessageProducer):
    message_context = context.Common(message.text, MainMenuKeyboardContext(UserRole.STUDENT))
    message_pack = MessagePack(
        message_context=message_context,
        message_recipients=[MessageRecipient(chat_id=320854517)]
    )
    await producer.produce(message_pack)
    await message.answer("Success")
