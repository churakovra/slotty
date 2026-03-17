import calendar

from app.keyboard.callback_factories.lesson import (
    LessonCreateCallback,
    LessonInfoCallback,
    LessonListCallback,
)
from app.keyboard.callback_factories.menu import ConfirmMenuCallback, MenuCallback
from app.keyboard.callback_factories.slot import (
    DaysForStudents,
    ResendSlotsCallback,
    SendSlots,
    SlotCreateCallback,
    SlotInfoCallback,
    SlotListCallback,
    SlotsForStudents,
)
from app.keyboard.callback_factories.student import (
    StudentCreateCallback,
    StudentInfoCallback,
    StudentListCallback,
)
from app.keyboard.callback_factories.teacher import TeacherCallback
from app.keyboard.markup import BotMarkup, MarkupButton, MarkupRow
from app.utils.bot_strings import BotStrings
from app.utils.datetime_utils import WEEKDAYS, day_format, time_format_HM
from app.utils.enums.bot_values import ActionType, WeekFlag
from app.utils.enums.menu_type import MenuType

from ..utils.datetime_utils import full_format_no_sec


def teacher_main_menu() -> BotMarkup:
    return BotMarkup(
        [
            MarkupRow(
                [
                    MarkupButton(
                        "Ученики", MenuCallback(menu_type=MenuType.TEACHER_STUDENT)
                    ),
                    MarkupButton(
                        "Окошки", MenuCallback(menu_type=MenuType.TEACHER_SLOT)
                    ),
                    MarkupButton(
                        "Предметы", MenuCallback(menu_type=MenuType.TEACHER_LESSON)
                    ),
                ]
            )
        ]
    )


def student_main_menu() -> BotMarkup:
    return BotMarkup(
        [
            MarkupRow(
                [
                    MarkupButton(
                        "Преподаватели",
                        MenuCallback(menu_type=MenuType.STUDENT_TEACHER),
                    ),
                    MarkupButton(
                        "Занятия", MenuCallback(menu_type=MenuType.STUDENT_SLOT)
                    ),
                ]
            )
        ]
    )


def admin_main_menu() -> BotMarkup:
    return BotMarkup(
        [
            MarkupRow(
                [
                    MarkupButton(
                        "Пока командами", MenuCallback(menu_type=MenuType.ADMIN_TEMP)
                    ),
                ]
            )
        ]
    )


def teacher_sub_menu_student() -> BotMarkup:
    return BotMarkup(
        [
            MarkupRow(
                [
                    MarkupButton("Мои ученики", StudentListCallback()),
                    MarkupButton("Добавить ученика", StudentCreateCallback()),
                ]
            ),
            MarkupRow(
                [
                    MarkupButton(
                        BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.TEACHER)
                    ),
                ]
            ),
        ]
    )


def teacher_sub_menu_slot() -> BotMarkup:
    return BotMarkup(
        [
            MarkupRow(
                [
                    MarkupButton("Моё расписание", SlotListCallback()),
                    MarkupButton("Добавить окошки", SlotCreateCallback()),
                ]
            ),
            MarkupRow(
                [
                    MarkupButton(
                        BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.TEACHER)
                    ),
                ]
            ),
        ]
    )


def teacher_sub_menu_lesson() -> BotMarkup:
    return BotMarkup(
        [
            MarkupRow(
                [
                    MarkupButton("Мои предметы", LessonListCallback()),
                    MarkupButton("Добавить предмет", LessonCreateCallback()),
                ]
            ),
            MarkupRow(
                [
                    MarkupButton(
                        BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.TEACHER)
                    ),
                ]
            ),
        ]
    )


def student_sub_menu_teacher(context) -> BotMarkup:
    return BotMarkup(
        [
            MarkupRow(
                [
                    MarkupButton("Заглушка", TeacherCallback(action=ActionType.LIST)),
                ]
            ),
            MarkupRow(
                [
                    MarkupButton(
                        BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.STUDENT)
                    ),
                ]
            ),
        ]
    )


def student_sub_menu_slot(context) -> BotMarkup:
    return BotMarkup(
        [
            MarkupRow(
                [
                    MarkupButton("Заглушка", SlotListCallback()),
                ]
            ),
            MarkupRow(
                [
                    MarkupButton(
                        BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.STUDENT)
                    ),
                ]
            ),
        ]
    )


def admin_sub_menu_temp(context) -> BotMarkup:
    return BotMarkup(
        [
            MarkupRow(
                [
                    MarkupButton(
                        "Пока командами", MenuCallback(menu_type=MenuType.ADMIN_TEMP)
                    ),
                ]
            ),
            MarkupRow(
                [
                    MarkupButton(
                        BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.ADMIN)
                    ),
                ]
            ),
        ]
    )


def parsed_slots(context) -> BotMarkup:
    return BotMarkup(
        [
            MarkupRow(
                [
                    MarkupButton(
                        BotStrings.Menu.YES, ConfirmMenuCallback(confirm=True)
                    ),
                    MarkupButton(
                        BotStrings.Menu.NO, ConfirmMenuCallback(confirm=False)
                    ),
                ]
            )
        ]
    )


def send_slots(context) -> BotMarkup:
    return BotMarkup(
        [
            MarkupRow(
                [
                    MarkupButton(
                        BotStrings.Menu.SEND,
                        SendSlots(teacher_uuid=context.teacher_uuid),
                    ),
                    MarkupButton(
                        BotStrings.Menu.CANCEL, MenuCallback(menu_type=MenuType.TEACHER)
                    ),
                ]
            )
        ]
    )


def days_for_students(context) -> BotMarkup:

    prev_slot_date = None
    rows: list[MarkupRow] = []
    for slot in context.slots:
        slot_date = slot.dt_start.date()
        if slot_date != prev_slot_date:
            day_number = calendar.weekday(
                slot_date.year, slot_date.month, slot_date.day
            )
            day_name = WEEKDAYS[day_number][2]
            callback_data = DaysForStudents(
                day=slot_date.strftime(day_format),
                teacher_uuid=context.teacher_uuid,
            )
            rows.append(
                MarkupRow(
                    [
                        MarkupButton(day_name, callback_data),
                    ]
                )
            )
            prev_slot_date = slot_date

    return BotMarkup(rows)


def slots_for_students(context) -> BotMarkup:
    rows = []
    for slot in context.slots:
        time_str = slot.dt_start.strftime(time_format_HM)
        rows.append(
            MarkupRow(
                [
                    MarkupButton(
                        time_str,
                        SlotsForStudents(uuid_slot=slot.uuid),
                    )
                ]
            )
        )
    rows.append(
        MarkupRow(
            [
                MarkupButton(
                    BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.STUDENT)
                )
            ]
        )
    )
    return BotMarkup(rows)


def success_slot_bind(context) -> BotMarkup:
    return BotMarkup(
        [
            MarkupRow(
                [
                    MarkupButton(
                        BotStrings.Menu.BIND_ANOTHER_SLOT,
                        ResendSlotsCallback(
                            teacher_uuid=context.teacher_uuid,
                            student_chat_id=context.student_chat_id,
                        ),
                    ),
                    MarkupButton(
                        BotStrings.Menu.MENU, MenuCallback(menu_type=MenuType.STUDENT)
                    ),
                ]
            )
        ]
    )


def specify_week(context) -> BotMarkup:
    return BotMarkup(
        [
            MarkupRow(
                [
                    MarkupButton(
                        BotStrings.Menu.CURRENT_WEEK,
                        context.callback_cls(week_flag=WeekFlag.CURRENT),
                    ),
                    MarkupButton(
                        BotStrings.Menu.NEXT_WEEK,
                        context.callback_cls(week_flag=WeekFlag.NEXT),
                    ),
                ]
            ),
            MarkupRow(
                [
                    MarkupButton(
                        BotStrings.Menu.BACK,
                        MenuCallback(menu_type=MenuType.TEACHER_SLOT),
                    ),
                ]
            ),
        ]
    )


def confirm_deletion(context) -> BotMarkup:
    # TODO think about NO callback. Maybe should use some 'decline callback' and only then in it's handler send menu to user
    return BotMarkup(
        [
            MarkupRow(
                [
                    MarkupButton(
                        BotStrings.Menu.YES,
                        context.callback_data_cls(
                            uuid=context.callback_data.uuid, confirmed=True
                        ),
                    ),
                    MarkupButton(
                        BotStrings.Menu.NO, MenuCallback(menu_type=MenuType.TEACHER)
                    ),
                ]
            )
        ]
    )


def specs_to_update(context) -> BotMarkup:
    context.specs["all"] = "Всё"
    return BotMarkup(
        [
            MarkupRow(
                [
                    MarkupButton(
                        label,
                        context.callback_data_cls(uuid=context.lesson_uuid, spec=spec),
                    )
                    for spec, label in context.specs.items()
                ]
            ),
            MarkupRow(
                [
                    MarkupButton(
                        BotStrings.Menu.BACK,
                        LessonListCallback(),
                    )
                ]
            ),
        ]
    )


def student_buttons(context) -> BotMarkup:
    rows = [
            MarkupRow(
                [
                    MarkupButton(
                        " ".join([student.firstname, student.lastname or ""]),
                        StudentInfoCallback(uuid=student.uuid),
                    )
                ]
            )
            for student in context.students
        ]
    rows.append(
        MarkupRow(
            [
                MarkupButton(BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.TEACHER_STUDENT))
            ]
        )
    )
    return BotMarkup(rows)


def lesson_buttons(context) -> BotMarkup:
    rows = [
            MarkupRow(
                [
                    MarkupButton(lesson.label, LessonInfoCallback(uuid=lesson.uuid))
                ]
            )
            for lesson in context.lessons
        ]
    rows.append(
        MarkupRow(
            [
                MarkupButton(BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.TEACHER_LESSON))
            ]
        )
    )
    return BotMarkup(rows)


def slot_buttons(context) -> BotMarkup:
    rows = [
            MarkupRow(
                [
                    MarkupButton(slot.dt_start.strftime(full_format_no_sec), SlotInfoCallback(uuid=slot.uuid))
                ]
            )
            for slot in context.slots
        ]
    rows.append(
        MarkupRow(
            [
                MarkupButton(BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.TEACHER_SLOT))
            ]
        )
    )
    return BotMarkup(rows)


def entity_operations(context) -> BotMarkup:
    rows = [
            MarkupRow(
                [
                    MarkupButton(name, allowed_operation(uuid=context.uuid))
                ]
            )
            for name, allowed_operation in context.operations[context.entity_type].items()
        ]
    rows.append(
        MarkupRow(
            [
                MarkupButton(BotStrings.Menu.CANCEL, MenuCallback(menu_type=MenuType.NEW))
            ]
        )
    )
    return BotMarkup(rows)


def lessons_to_assign(context) -> BotMarkup:
    rows = [
            MarkupRow(
                [
                    MarkupButton(
                        lesson.label,
                        context.assign_callback(
                            uuid=context.student_uuid,
                            id_lesson=lesson.id,
                        ),
                    )
                ]
            )
            for lesson in context.lessons
        ]
    rows.append(
        MarkupRow(
            [
                MarkupButton(BotStrings.Menu.CANCEL, MenuCallback(menu_type=MenuType.TEACHER_STUDENT))
            ]
        )
    )
    return BotMarkup(rows)


def cancel_markup(context) -> BotMarkup:
    return BotMarkup(
        [
            MarkupRow(
                [
                    MarkupButton(BotStrings.Menu.CANCEL, MenuCallback(menu_type=MenuType.CANCEL)),
                ]
            )
        ]
    )
