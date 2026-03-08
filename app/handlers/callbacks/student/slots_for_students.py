from uuid import UUID

from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboard.callback_factories.slot import SlotsForStudents
from app.keyboard.context import UserRole
from app.message import context
from app.schemas.slot import SlotDTO
from app.schemas.user import UserDTO
from app.services.slot_service import SlotService
from app.services.teacher_service import TeacherService
from app.utils.datetime_utils import full_format_no_sec

router = Router()


@router.callback_query(SlotsForStudents.filter())
async def handle_callback(
    callback: CallbackQuery,
    callback_data: SlotsForStudents,
    session: AsyncSession,
    user: UserDTO,
):
    slot_uuid = callback_data.uuid_slot
    assigned_slot = await assign_slot(
        session=session, student=user, slot_uuid=slot_uuid
    )
    teacher_service = TeacherService(session=session)
    teacher = await teacher_service.get_teacher_by_uuid(
        teacher_uuid=assigned_slot.uuid_teacher
    )

    slot_time = assigned_slot.dt_start.strftime(full_format_no_sec)
    # await notify_student(
    #     teacher=teacher, student=user, slot_time=slot_time, notifier=notifier
    # )
    # await notify_teacher(
    #     teacher=teacher, student=user, slot_time=slot_time, notifier=notifier
    # )

    await callback.message.delete()
    await callback.answer()


async def assign_slot(
    session: AsyncSession,
    student: UserDTO,
    slot_uuid: UUID,
) -> SlotDTO:
    slot_service = SlotService(session=session)
    return await slot_service.assign_slot(
        student_uuid=student.uuid, slot_uuid=slot_uuid
    )


async def notify_student(teacher: UserDTO, student: UserDTO, slot_time: str) -> None:
    message_context = context.SlotTakenByStudent(
        teacher.uuid, student.chat_id, UserRole.STUDENT, teacher.username
    )

    # TODO send message via notifier service

    # await notifier.send_message(
    #     bot_message=bot_message, receiver_chat_id=student.chat_id
    # )


async def notify_teacher(teacher: UserDTO, student: UserDTO, slot_time: str) -> None:
    message_context = context.NotifyTeacherSlotTaken(student.username, slot_time)

    # TODO send message via notifier service

    # await notifier.send_message(
    #     bot_message=notify_teacher_message, receiver_chat_id=teacher.chat_id
    # )
