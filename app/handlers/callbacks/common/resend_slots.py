from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboard.callback_factories.slot import ResendSlotsCallback
from app.message import context, message_builder
from app.services.slot_service import SlotService

router = Router()


@router.callback_query(ResendSlotsCallback.filter())
async def handle_callback(
    callback: CallbackQuery,
    callback_data: ResendSlotsCallback,
    session: AsyncSession,
) -> None:
    slots_service = SlotService(session)
    slots = await slots_service.get_free_slots(callback_data.teacher_uuid)
    message_context = context.DaysForStudents(callback_data.teacher_uuid, slots)
    await callback.message.answer(**message_builder.build(message_context))
    await callback.answer()
