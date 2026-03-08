from app.keyboard.builder import markup_builder
from app.message.context import (
    Common,
    ConfirmOperation,
    DaysForStudents,
    EntitiesList,
    Greeting,
    LessonInfo,
    MainMenu,
    NotifyTeacherSlotTaken,
    ParsedSlots,
    SlotInfo,
    SlotTakenByStudent,
    SpecifyWeek,
    Statistics,
    StudentAssign,
    StudentInfo,
)
from app.message.utils import (
    get_lesson_info,
    get_slot_info,
    get_slots_schedule_reply,
    get_student_info,
    slots_to_reply,
)
from app.schemas.message import BotMessage
from app.utils.bot_strings import BotStrings


def common(context: Common) -> BotMessage:
    text = context.text
    markup = (
        markup_builder.build(context.markup_context) if context.markup_context else None
    )
    return BotMessage(text=text, reply_markup=markup)


def greeting(context: Greeting) -> BotMessage:
    text = BotStrings.Common.GREETING
    return BotMessage(text=text, reply_markup=None)


def main_menu_message(context: MainMenu) -> BotMessage:
    text = BotStrings.Common.MENU
    markup = markup_builder.build(context.markup_context)
    return BotMessage(
        text=text,
        reply_markup=markup,
    )


def parsed_slots_message(context: ParsedSlots) -> BotMessage:
    text = slots_to_reply(context.slots)
    markup = markup_builder.build(context.markup_context)
    return BotMessage(text=text, reply_markup=markup)


def entities_list(context: EntitiesList) -> BotMessage:
    text = context.text
    markup = markup_builder.build(context.markup_context)
    return BotMessage(text=text, reply_markup=markup)


def student_info(context: StudentInfo) -> BotMessage:
    text = get_student_info(context.student, context.lessons)
    markup = markup_builder.build(context.markup_context)
    return BotMessage(text=text, reply_markup=markup)


def slot_info(context: SlotInfo) -> BotMessage:
    text = get_slot_info(context.slot)
    markup = markup_builder.build(context.markup_context)
    return BotMessage(text=text, reply_markup=markup)


def lesson_info(context: LessonInfo) -> BotMessage:
    text = get_lesson_info(context.lesson)
    markup = markup_builder.build(context.markup_context)
    return BotMessage(text=text, reply_markup=markup, parse_mode="MarkdownV2")


def confirm_operation(context: ConfirmOperation) -> BotMessage:
    text = BotStrings.Common.CONFIRM_OPERATION
    markup = markup_builder.build(context.markup_context)
    return BotMessage(text=text, reply_markup=markup)


def student_assign(context: StudentAssign) -> BotMessage:
    text = BotStrings.Teacher.STUDENT_ATTACH_LESSONS_LIST
    markup = markup_builder.build(context.markup_context)
    return BotMessage(text=text, reply_markup=markup)


def specify_week(context: SpecifyWeek) -> BotMessage:
    text = BotStrings.Common.SPECIFY_WEEK
    markup = markup_builder.build(context.markup_context)
    return BotMessage(text=text, reply_markup=markup)


def statistics(context: Statistics) -> BotMessage:
    text = get_slots_schedule_reply(context.slots, context.lessons, context.students)
    markup = markup_builder.build(context.markup_context)
    return BotMessage(text=text, reply_markup=markup, parse_mode="MarkdownV2")

def days_for_students(context: DaysForStudents) -> BotMessage:
    text = slots_to_reply(context.slots)
    markup = markup_builder.build(context.markup_context)
    return BotMessage(text=text, reply_markup=markup)


def slot_taken_by_student(context: SlotTakenByStudent) -> BotMessage:
    text = BotStrings.Student.SLOTS_ASSIGN_SUCCESS
    markup = markup_builder.build(context.markup_context)
    return BotMessage(text=text, reply_markup=markup)


def notify_teacher_slot_taken(context: NotifyTeacherSlotTaken) -> BotMessage:
    text = BotStrings.Teacher.SLOT_IS_TAKEN % (context.student_username, context.slot_time)
    return BotMessage(text=text)