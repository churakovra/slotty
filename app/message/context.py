from collections.abc import Callable
from dataclasses import dataclass
from uuid import UUID

from app.keyboard.callback_factories.common import (
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
from app.message.fabric import (
    common,
    confirm_operation,
    days_for_students,
    entities_list,
    greeting,
    lesson_info,
    main_menu_message,
    notify_teacher_slot_taken,
    parsed_slots_message,
    slot_info,
    slot_taken_by_student,
    specify_week,
    statistics,
    student_assign,
    student_info,
)
from app.schemas.lesson import LessonDTO
from app.schemas.message import BotMessage
from app.schemas.slot import SlotDTO
from app.schemas.student import StudentDTO
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import EntityType, UserRole


class AbstractBotMessageContext:
    fabric: Callable[..., BotMessage]

@dataclass
class Common(AbstractBotMessageContext):
    fabric = common
    text: str
    markup_context: AbstractMarkupContext | None = None


@dataclass
class Greeting(AbstractBotMessageContext):
    fabric = greeting
    pass


@dataclass
class MainMenu(AbstractBotMessageContext):
    fabric = main_menu_message
    user_role: UserRole

    @property
    def markup_context(self) -> MainMenuKeyboardContext:
        return MainMenuKeyboardContext(self.user_role)


@dataclass
class ParsedSlots(AbstractBotMessageContext):
    fabric = parsed_slots_message
    slots: list[SlotDTO]
    markup_context = ParsedSlotsKeyboardContext()


@dataclass
class EntitiesList(AbstractBotMessageContext):
    fabric = entities_list
    entities: list
    entity_type: EntityType

    @property
    def text(self) -> str:
        entity_type_to_text = {
            EntityType.LESSON: BotStrings.Teacher.TEACHER_LESSON_LIST,
            EntityType.SLOT: BotStrings.Teacher.SLOTS_LIST,
            EntityType.STUDENT: BotStrings.Teacher.TEACHER_STUDENTS_LIST,
        }
        return entity_type_to_text[self.entity_type]

    @property
    def markup_context(self) -> EntitiesListKeyboardContext:
        return EntitiesListKeyboardContext(
            self.entities,
            self.entity_type,
        )


@dataclass
class StudentInfo(AbstractBotMessageContext):
    fabric = student_info
    student: StudentDTO
    lessons: list[LessonDTO]

    @property
    def markup_context(self) -> EntityOperationsKeyboardContext:
        return EntityOperationsKeyboardContext(self.student.uuid, EntityType.STUDENT)


@dataclass
class SlotInfo(AbstractBotMessageContext):
    fabric = slot_info
    slot: SlotDTO

    @property
    def markup_context(self) -> EntityOperationsKeyboardContext:
        return EntityOperationsKeyboardContext(self.slot.uuid, EntityType.SLOT)


@dataclass
class LessonInfo(AbstractBotMessageContext):
    fabric = lesson_info
    lesson: LessonDTO

    @property
    def markup_context(self) -> EntityOperationsKeyboardContext:
        return EntityOperationsKeyboardContext(self.lesson.uuid, EntityType.LESSON)



@dataclass
class ConfirmOperation(AbstractBotMessageContext):
    fabric = confirm_operation
    operation_callback: type[BaseOperationCallback]
    callback_data: BaseOperationCallback

    @property
    def markup_context(self) -> ConfirmDeletionKeyboardContext:
        # TODO add update confirm callbacks
        delete_callbacks = [
            StudentDeleteCallback,
            SlotDeleteCallback,
            LessonDeleteCallback,
        ]
        if self.operation_callback in delete_callbacks:
            return ConfirmDeletionKeyboardContext(
                self.operation_callback, self.callback_data
            )
        else:
            raise Exception(f"Unknown operation {self.operation_callback}")


@dataclass
class StudentAssign(AbstractBotMessageContext):
    fabric = student_assign
    student_uuid: UUID
    lessons: list[LessonDTO]

    @property
    def markup_context(self) -> LessonsAssignKeyboardContext:
        return LessonsAssignKeyboardContext(
            self.student_uuid, StudentAssignCallback, self.lessons
        )


@dataclass
class SpecifyWeek(AbstractBotMessageContext):
    fabric = specify_week
    callback_cls: type[SpecifyWeekMixin]

    @property
    def markup_context(self) -> SpecifyWeekKeyboardContext:
        return SpecifyWeekKeyboardContext(self.callback_cls)


@dataclass
class Statistics(AbstractBotMessageContext):
    fabric = statistics
    markup_context = CancelKeyboardContext()
    slots: list[SlotDTO]
    lessons: list[LessonDTO]
    students: list[StudentDTO]


@dataclass
class DaysForStudents(AbstractBotMessageContext):
    fabric = days_for_students
    teacher_uuid: UUID
    slots: list[SlotDTO]

    @property
    def markup_context(self) -> DaysForStudentsKeyboardContext:
        return DaysForStudentsKeyboardContext(self.teacher_uuid, self.slots)
    

@dataclass
class SlotTakenByStudent(AbstractBotMessageContext):
    fabric = slot_taken_by_student
    teacher_uuid: UUID
    student_chat_id: int
    role: UserRole
    teacher_username: str

    @property
    def markup_context(self):
        return SuccessSlotBindKeyboardContext(
            teacher_uuid=self.teacher_uuid,
            student_chat_id=self.student_chat_id,
            role=self.role,
            username=self.teacher_username,
        )
    

@dataclass
class NotifyTeacherSlotTaken(AbstractBotMessageContext):
    fabric = notify_teacher_slot_taken
    student_username: str
    slot_time: str