from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboard.context import CancelKeyboardContext
from app.message import message_builder
from app.message.context import Common
from app.services.lesson_service import LessonService
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import ActionType
from app.utils.logger import setup_logger

router = Router()
logger = setup_logger(__name__)


@router.message(ScheduleStates.wait_for_teacher_lesson_price)
async def handle_state(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
):
    data = await state.get_data()
    previous_message_id = data["previous_message_id"]
    operation_type = data["operation_type"]
    raw_mt = getattr(message, "text", "")

    label = data["lesson_label"]
    duration = data["lesson_duration"]
    price = int(raw_mt.strip())
    uuid_teacher = data["uuid_teacher"]

    try:
        lesson_service = LessonService(session)
        if operation_type == ActionType.CREATE:
            await lesson_service.create_lesson(
                label=label, duration=duration, uuid_teacher=uuid_teacher, price=price
            )
            response_msg = BotStrings.Teacher.TEACHER_LESSON_ADD_SUCCESS
        else:
            uuid_lesson = data["uuid_lesson"]
            await lesson_service.update_lesson(
                lesson_uuid=uuid_lesson, label=label, duration=duration, price=price
            )
            response_msg = BotStrings.Teacher.TEACHER_LESSON_UPDATE_SUCCESS

        message_context = Common(
            text=response_msg,
            markup_context=CancelKeyboardContext(),
        )
        await message.answer(**message_builder.build(message_context))
        await state.clear()

        logger.info(f"Teacher {uuid_teacher} added new lesson")
    except Exception:
        logger.error(type)

        sent_message = await message.answer(
            BotStrings.Teacher.TEACHER_LESSON_ADD_PRICE_ERROR
        )
        await state.update_data(previous_message_id=sent_message.message_id)
        await state.set_state(ScheduleStates.wait_for_teacher_lesson_price)

    finally:
        await message.chat.delete_message(message_id=previous_message_id)
        await message.delete()
