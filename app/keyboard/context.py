from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from app.keyboard.callback_factories.common import (
    BaseAssignCallback,
    BaseDeleteCallback,
    BaseOperationCallback,
    BaseUpdateCallback,
)
from app.keyboard.callback_factories.lesson import (
    LessonDeleteCallback,
    LessonUpdateCallback,
)
from app.keyboard.callback_factories.mixins import SpecifyWeekMixin
from app.keyboard.callback_factories.slot import SlotDeleteCallback, SlotUpdateCallback
from app.keyboard.callback_factories.student import (
    StudentAssignCallback,
    StudentDeleteCallback,
    StudentDetachCallback,
)
from app.keyboard.fabric import (
    admin_main_menu,
    admin_sub_menu_temp,
    cancel_markup,
    confirm_deletion,
    days_for_students,
    entity_operations,
    lesson_buttons,
    lessons_to_assign,
    parsed_slots,
    send_slots,
    slot_buttons,
    slots_for_students,
    specify_week,
    specs_to_update,
    student_buttons,
    student_main_menu,
    student_sub_menu_slot,
    student_sub_menu_teacher,
    success_slot_bind,
    teacher_main_menu,
    teacher_sub_menu_lesson,
    teacher_sub_menu_slot,
    teacher_sub_menu_student,
)
from app.schemas.lesson import LessonDTO
from app.schemas.slot import SlotDTO
from app.schemas.student import StudentDTO
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import EntityType, UserRole


class AbstractMarkupContext:
    fabric: Callable[..., tuple[list[Any], int]]


@dataclass
class MainMenuKeyboardContext(AbstractMarkupContext):
    user_role: UserRole

    @property
    def fabric(self):
        menu_by_role = {
            UserRole.TEACHER: teacher_main_menu,
            UserRole.STUDENT: student_main_menu,
            UserRole.ADMIN: admin_main_menu,
        }
        return menu_by_role[self.user_role]


@dataclass
class SubMenuKeyboardContext(AbstractMarkupContext):
    user_role: UserRole
    entity_type: EntityType

    @property
    def fabric(self):
        menu_by_role_entity = {
            UserRole.TEACHER: {
                EntityType.STUDENT: teacher_sub_menu_student,
                EntityType.SLOT: teacher_sub_menu_slot,
                EntityType.LESSON: teacher_sub_menu_lesson,
            },
            UserRole.STUDENT: {
                EntityType.TEACHER: student_sub_menu_teacher,
                EntityType.SLOT: student_sub_menu_slot,
            },
            UserRole.ADMIN: {
                EntityType.UNKNOWN: admin_sub_menu_temp,
            },
        }
        return menu_by_role_entity[self.user_role][self.entity_type]


@dataclass
class ParsedSlotsKeyboardContext(AbstractMarkupContext):
    fabric = parsed_slots


@dataclass
class CancelKeyboardContext(AbstractMarkupContext):
    fabric = cancel_markup


@dataclass
class SendSlotsKeyboardContext(AbstractMarkupContext):
    fabric = send_slots
    teacher_uuid: UUID


@dataclass
class DaysForStudentsKeyboardContext(AbstractMarkupContext):
    fabric = days_for_students
    teacher_uuid: UUID
    slots: list[SlotDTO]


@dataclass
class SlotsForStudentsKeyboardContext(AbstractMarkupContext):
    fabric = slots_for_students
    teacher_uuid: UUID
    slots: list[SlotDTO]


@dataclass
class SuccessSlotBindKeyboardContext(AbstractMarkupContext):
    fabric = success_slot_bind
    teacher_uuid: UUID
    student_chat_id: int
    username: str
    role: UserRole


@dataclass
class SpecifyWeekKeyboardContext(AbstractMarkupContext):
    fabric = specify_week
    callback_cls: type[SpecifyWeekMixin]


@dataclass
class EntitiesListKeyboardContext(AbstractMarkupContext):
    entities: list
    entity_type: EntityType

    @property
    def fabric(self):
        buttons_by_entity_type = {
            EntityType.STUDENT: student_buttons,
            EntityType.LESSON: lesson_buttons,
            EntityType.SLOT: slot_buttons,
        }
        return buttons_by_entity_type[self.entity_type]

    @property
    def students(self) -> list[StudentDTO]:
        return self.entities

    @property
    def lessons(self) -> list[LessonDTO]:
        return self.entities

    @property
    def slots(self) -> list[SlotDTO]:
        return self.entities


@dataclass
class EntityOperationsKeyboardContext(AbstractMarkupContext):
    fabric = entity_operations
    uuid: UUID
    entity_type: EntityType

    @property
    def operations(self) -> dict[EntityType, dict[str, Any]]:
        return {
            EntityType.STUDENT: {
                BotStrings.Menu.ATTACH: StudentAssignCallback,
                BotStrings.Menu.DETACH: StudentDetachCallback,
                BotStrings.Menu.DELETE: StudentDeleteCallback,
            },
            EntityType.LESSON: {
                BotStrings.Menu.UPDATE: LessonUpdateCallback,
                BotStrings.Menu.DELETE: LessonDeleteCallback,
            },
            EntityType.SLOT: {
                BotStrings.Menu.UPDATE: SlotUpdateCallback,
                BotStrings.Menu.DELETE: SlotDeleteCallback,
            },
        }


@dataclass
class StudentOperationKeyboardContext(AbstractMarkupContext):
    students: list[StudentDTO]
    operation_callback_cls: type[BaseOperationCallback]


@dataclass
class LessonOperationKeyboardContext(AbstractMarkupContext):
    lessons: list[LessonDTO]
    operation_callback_cls: type[BaseOperationCallback]


@dataclass
class ConfirmDeletionKeyboardContext(AbstractMarkupContext):
    fabric = confirm_deletion
    callback_data_cls: type[BaseDeleteCallback]
    callback_data: BaseDeleteCallback


@dataclass
class SpecsToUpdateKeyboardContext(AbstractMarkupContext):
    fabric = specs_to_update
    lesson_uuid: UUID
    specs: dict[str, str]
    callback_data_cls: type[BaseUpdateCallback]


@dataclass
class LessonsAssignKeyboardContext(AbstractMarkupContext):
    fabric = lessons_to_assign
    student_uuid: UUID
    assign_callback: type[BaseAssignCallback]
    lessons: list[LessonDTO]
