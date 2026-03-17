from dataclasses import dataclass
from uuid import UUID

from app.keyboard.callback_factories.common import (
    BaseDeleteCallback,
    BaseOperationCallback,
)
from app.keyboard.callback_factories.lesson import LessonDeleteCallback
from app.keyboard.callback_factories.mixins import SpecifyWeekMixin
from app.keyboard.callback_factories.slot import SlotDeleteCallback
from app.keyboard.callback_factories.student import (
    StudentAssignCallback,
    StudentDeleteCallback,
)
from app.keyboard.context import (
    AbstractMarkupContext,
    CancelKeyboardContext,
    ConfirmDeletionKeyboardContext,
    DaysForStudentsKeyboardContext,
    EntitiesListKeyboardContext,
    EntityOperationsKeyboardContext,
    LessonsAssignKeyboardContext,
    MainMenuKeyboardContext,
    ParsedSlotsKeyboardContext,
    SpecifyWeekKeyboardContext,
    SuccessSlotBindKeyboardContext,
)
from app.message.utils import (
    get_lesson_info,
    get_slot_info,
    get_slots_schedule_reply,
    get_student_info,
    slots_to_reply,
)
from app.schemas.lesson import LessonDTO
from app.schemas.slot import SlotDTO
from app.schemas.student import StudentDTO
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import EntityType, UserRole


class AbstractBotMessageContext:
    def __init__(
        self,
        text: str,
        markup_context: AbstractMarkupContext | None = None,
        parse_mode: str | None = None,
    ) -> None:
        self.text = text
        self.markup_context = markup_context
        self.parse_mode = parse_mode

    def to_dict(self):
        return {
            "text": self.text,
            "markup_context": self.markup_context.to_dict(),
            "parse_mode": self.parse_mode(),
        }


class MainMenu(AbstractBotMessageContext):
    def __init__(self, user_role: UserRole) -> None:
        super().__init__(BotStrings.Common.MENU)
        self.user_role = user_role
        self.markup_context = MainMenuKeyboardContext(user_role)


class Common(AbstractBotMessageContext):
    pass


class Greeting(AbstractBotMessageContext):
    def __init__(self):
        super().__init__(BotStrings.Common.GREETING)


class ParsedSlots(AbstractBotMessageContext):
    def __init__(self, slots: list[SlotDTO]) -> None:
        super().__init__(slots_to_reply(slots))
        self.markup_context = ParsedSlotsKeyboardContext()


class EntitiesList(AbstractBotMessageContext):
    def __init__(self, entities: list, entity_type: EntityType) -> None:
        super().__init__(self._define_text(entity_type))
        self.markup_context = EntitiesListKeyboardContext(entities, entity_type)

    def _define_text(self, entity_type) -> str:
        entity_type_to_text = {
            EntityType.LESSON: BotStrings.Teacher.TEACHER_LESSON_LIST,
            EntityType.SLOT: BotStrings.Teacher.SLOTS_LIST,
            EntityType.STUDENT: BotStrings.Teacher.TEACHER_STUDENTS_LIST,
        }
        return entity_type_to_text[entity_type]

class ConfirmOperation(AbstractBotMessageContext):
    def __init__(
        self, operation_callback: BaseOperationCallback, callback_data
    ) -> None:
        super().__init__(BotStrings.Common.CONFIRM_OPERATION)
        self._define_markup_context(operation_callback, callback_data)

    def _define_markup_context(
        self,
        operation_callback: BaseOperationCallback,
        callback_data: BaseDeleteCallback,
    ) -> None:
        # TODO add update confirm callbacks
        delete_callbacks = [
            StudentDeleteCallback,
            SlotDeleteCallback,
            LessonDeleteCallback,
        ]
        if operation_callback not in delete_callbacks:
            raise Exception(f"Unknown operation {operation_callback}")
        self.markup_context = ConfirmDeletionKeyboardContext(
            operation_callback, callback_data
        )


class StudentAssign(AbstractBotMessageContext):
    def __init__(self, student_uuid: UUID, lessons: list[LessonDTO]) -> None:
        super().__init__(BotStrings.Teacher.STUDENT_ATTACH_LESSONS_LIST)
        self.markup_context = LessonsAssignKeyboardContext(
            student_uuid, StudentAssignCallback, lessons
        )


class SpecifyWeek(AbstractBotMessageContext):
    def __init__(self, callback_cls: type[SpecifyWeekMixin]) -> None:
        super().__init__(BotStrings.Common.SPECIFY_WEEK)
        self.markup_context = SpecifyWeekKeyboardContext(callback_cls)


class Statistics(AbstractBotMessageContext):
    def __init__(
        self, slots: list[SlotDTO], lessons: list[LessonDTO], students: list[StudentDTO]
    ) -> None:
        super().__init__(get_slots_schedule_reply(slots, lessons, students))
        self.markup_context = CancelKeyboardContext()
        self.parse_mode = "MarkdownV2"


class DaysForStudents(AbstractBotMessageContext):
    def __init__(self, teacher_uuid: UUID, slots: list[SlotDTO]) -> None:
        super().__init__(slots_to_reply(slots))
        self.markup_context = DaysForStudentsKeyboardContext(teacher_uuid, slots)


@dataclass
class SlotTakenByStudent(AbstractBotMessageContext):
    def __init__(
        self,
        teacher_uuid: UUID,
        student_chat_id: int,
        role: UserRole,
        teacher_username: str,
    ) -> None:
        super().__init__(BotStrings.Student.SLOTS_ASSIGN_SUCCESS)
        self.markup_context = SuccessSlotBindKeyboardContext(
            teacher_uuid=teacher_uuid,
            student_chat_id=student_chat_id,
            role=role,
            username=teacher_username,
        )

@dataclass
class NotifyTeacherSlotTaken(AbstractBotMessageContext):
    def __init__(self, student_username: str, slot_time: str) -> None:
        super().__init__(
            BotStrings.Teacher.SLOT_IS_TAKEN
            % (
                student_username,
                slot_time,
            )
        )
