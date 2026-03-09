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
from app.utils.bot_strings import BotStrings
from app.utils.datetime_utils import WEEKDAYS, day_format, time_format_HM
from app.utils.enums.bot_values import ActionType, WeekFlag
from app.utils.enums.menu_type import MenuType

from ..utils.datetime_utils import full_format_no_sec


def teacher_main_menu(context) -> tuple[list, int]:
    buttons = [
        ("Ученики", MenuCallback(menu_type=MenuType.TEACHER_STUDENT)),
        ("Окошки", MenuCallback(menu_type=MenuType.TEACHER_SLOT)),
        ("Предметы", MenuCallback(menu_type=MenuType.TEACHER_LESSON)),
    ]
    adjust = 1
    return buttons, adjust


def student_main_menu(context) -> tuple[list, int]:
    buttons = [
        ("Преподаватели", MenuCallback(menu_type=MenuType.STUDENT_TEACHER)),
        ("Занятия", MenuCallback(menu_type=MenuType.STUDENT_SLOT)),
    ]
    adjust = 1
    return buttons, adjust


def admin_main_menu(context) -> tuple[list, int]:
    buttons = [
        ("Пока командами", MenuCallback(menu_type=MenuType.ADMIN_TEMP)),
    ]
    adjust = 1
    return buttons, adjust


def teacher_sub_menu_student(context) -> tuple[list, int]:
    buttons = [
        ("Мои ученики", StudentListCallback()),
        ("Добавить ученика", StudentCreateCallback()),
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.TEACHER)),
    ]
    adjust = 1
    return buttons, adjust


def teacher_sub_menu_slot(context) -> tuple[list, int]:
    buttons = [
        ("Моё расписание", SlotListCallback()),
        ("Добавить окошки", SlotCreateCallback()),
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.TEACHER)),
    ]
    adjust = 1
    return buttons, adjust


def teacher_sub_menu_lesson(context) -> tuple[list, int]:
    buttons = [
        ("Мои предметы", LessonListCallback()),
        ("Добавить предмет", LessonCreateCallback()),
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.TEACHER)),
    ]
    adjust = 1
    return buttons, adjust


def student_sub_menu_teacher(context) -> tuple[list, int]:
    buttons = [
        ("Заглушка", TeacherCallback(action=ActionType.LIST)),
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.STUDENT)),
    ]
    adjust = 1
    return buttons, adjust


def student_sub_menu_slot(context) -> tuple[list, int]:
    buttons = [
        ("Заглушка", SlotListCallback()),
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.STUDENT)),
    ]
    adjust = 1
    return buttons, adjust


def admin_sub_menu_temp(context) -> tuple[list, int]:
    buttons = [
        ("Пока командами", MenuCallback(menu_type=MenuType.ADMIN_TEMP)),
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.ADMIN)),
    ]
    adjust = 1
    return buttons, adjust


def parsed_slots(context) -> tuple[list, int]:
    buttons = [
        (BotStrings.Menu.YES, ConfirmMenuCallback(confirm=True)),
        (BotStrings.Menu.NO, ConfirmMenuCallback(confirm=False)),
    ]
    adjust = 2
    return buttons, adjust


def send_slots(context) -> tuple[list, int]:
    buttons = [
        (BotStrings.Menu.SEND, SendSlots(teacher_uuid=context.teacher_uuid)),
        (BotStrings.Menu.CANCEL, MenuCallback(menu_type=MenuType.TEACHER)),
    ]
    adjust = 1
    return buttons, adjust


def days_for_students(context) -> tuple[list, int]:
    prev_slot_date = None
    buttons = []
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
            buttons.append((day_name, callback_data))
            prev_slot_date = slot_date
    adjust = 1
    return buttons, adjust


def slots_for_students(context) -> tuple[list, int]:
    buttons = []
    for slot in context.slots:
        time_str = slot.dt_start.strftime(time_format_HM)
        buttons.append((time_str, SlotsForStudents(uuid_slot=slot.uuid)))
    buttons.append((BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.STUDENT)))
    adjust = 1
    return buttons, adjust


def success_slot_bind(context) -> tuple[list, int]:
    buttons = [
        (
            BotStrings.Menu.BIND_ANOTHER_SLOT,
            ResendSlotsCallback(
                teacher_uuid=context.teacher_uuid,
                student_chat_id=context.student_chat_id,
            ),
        ),
        (BotStrings.Menu.MENU, MenuCallback(menu_type=MenuType.STUDENT)),
    ]
    adjust = 1
    return buttons, adjust


def specify_week(context) -> tuple[list, int]:
    buttons = [
        (
            BotStrings.Menu.CURRENT_WEEK,
            context.callback_cls(week_flag=WeekFlag.CURRENT),
        ),
        (BotStrings.Menu.NEXT_WEEK, context.callback_cls(week_flag=WeekFlag.NEXT)),
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.TEACHER_SLOT)),
    ]
    adjust = 2
    return buttons, adjust


def confirm_deletion(context) -> tuple[list, int]:
    # TODO think about NO callback. Maybe should use some 'decline callback' and only then in it's handler send menu to user
    buttons = [
        (
            BotStrings.Menu.YES,
            context.callback_data_cls(uuid=context.callback_data.uuid, confirmed=True),
        ),
        (BotStrings.Menu.NO, MenuCallback(menu_type=MenuType.TEACHER)),
    ]
    adjust = 2
    return buttons, adjust


def specs_to_update(context) -> tuple[list, int]:
    context.specs["all"] = "Всё"
    buttons = [
        (label, context.callback_data_cls(uuid=context.lesson_uuid, spec=spec))
        for spec, label in context.specs.items()
    ]
    buttons.append((BotStrings.Menu.BACK, LessonListCallback()))
    adjust = 1
    return buttons, adjust


def student_buttons(context) -> tuple[list, int]:
    buttons = [
        (
            " ".join([student.firstname, student.lastname or ""]),
            StudentInfoCallback(uuid=student.uuid),
        )
        for student in context.students
    ]
    buttons.append(
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.TEACHER_STUDENT))
    )
    adjust = 1
    return buttons, adjust


def lesson_buttons(context) -> tuple[list, int]:
    buttons = [
        (lesson.label, LessonInfoCallback(uuid=lesson.uuid))
        for lesson in context.lessons
    ]
    buttons.append(
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.TEACHER_LESSON))
    )
    adjust = 1
    return buttons, adjust


def slot_buttons(context) -> tuple[list, int]:
    buttons = [
        (slot.dt_start.strftime(full_format_no_sec), SlotInfoCallback(uuid=slot.uuid))
        for slot in context.slots
    ]
    buttons.append(
        (BotStrings.Menu.BACK, MenuCallback(menu_type=MenuType.TEACHER_SLOT))
    )
    adjust = 1
    return buttons, adjust


def entity_operations(context) -> tuple[list, int]:
    buttons = [
        (name, allowed_operation(uuid=context.uuid))
        for name, allowed_operation in context.operations[context.entity_type].items()
    ]
    buttons.append((BotStrings.Menu.CANCEL, MenuCallback(menu_type=MenuType.NEW)))
    adjust = 1
    return buttons, adjust


def lessons_to_assign(context) -> tuple[list, int]:
    buttons = [
        (
            lesson.label,
            context.assign_callback(
                uuid=context.student_uuid,
                id_lesson=lesson.id,
            ),
        )
        for lesson in context.lessons
    ]
    buttons.append(
        (BotStrings.Menu.CANCEL, MenuCallback(menu_type=MenuType.TEACHER_STUDENT))
    )
    adjust = 1
    return buttons, adjust


def cancel_markup(context) -> tuple[list, int]:
    buttons = [(BotStrings.Menu.CANCEL, MenuCallback(menu_type=MenuType.CANCEL))]
    adjust = 1
    return buttons, adjust
