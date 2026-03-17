from dataclasses import dataclass, field
from typing import Any

from app.keyboard.fabric import (
    admin_main_menu,
    entity_operations,
    student_main_menu,
    teacher_main_menu,
)
from app.keyboard.markup import BotMarkup
from app.message.utils import get_lesson_info, get_slot_info, get_student_info
from app.schemas.lesson import LessonDTO
from app.schemas.slot import SlotDTO
from app.schemas.student import StudentDTO
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import UserRole

"""
BotMessage: {
    "text": str,
    "markup": {
        "rows": [
            [{"text": str, "callback": str}, {"text": str, "callback": str}],
            [{"text": str, "callback": str}, {"text": str, "callback": str}],
        ]
    },
    "parse_mode": str | None
}
"""


@dataclass
class BotMessage:
    text: str
    markup: BotMarkup | None = field(default=None)
    parse_mode: str | None = field(default=None)

    def prepare(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "reply_markup": self.markup.build(),
            "parse_mode": self.parse_mode,
        }

    @classmethod
    def main_menu(cls, user_role: UserRole):
        markup_by_role = {
            UserRole.TEACHER: teacher_main_menu,
            UserRole.STUDENT: student_main_menu,
            UserRole.ADMIN: admin_main_menu,
        }
        markup = markup_by_role[user_role]()
        return cls(
            text=BotStrings.Common.MENU,
            markup=markup,
        )

    @classmethod
    def entity_info(cls, entity, **kwargs):
        info_by_entity = {
            type[StudentDTO]: get_student_info,
            type[SlotDTO]: get_slot_info,
            type[LessonDTO]: get_lesson_info,
        }
        parse_mode = "MarkdownV2" if isinstance(entity, LessonDTO) else None
        return cls(
            text=info_by_entity[type(entity)](entity, **kwargs),
            markup=entity_operations(entity.uuid, type(entity)),
            parse_mode=parse_mode,
        )
