from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.message import context, message_builder
from app.notifier.producer import MessageProducer
from app.utils.logger import setup_logger

router = Router()
logger = setup_logger(__name__)


@router.message(Command("produce"))
async def produce(message: Message, producer: MessageProducer):
    message_context = context.Common(message.text)
    await producer.produce(message_builder.build(message_context))
    await message.answer("Success")
