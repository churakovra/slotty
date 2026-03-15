from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.keyboard.callback_factories.menu import MenuCallback
from app.keyboard.context import (
    EntityType,
    MainMenuKeyboardContext,
    SubMenuKeyboardContext,
    UserRole,
)
from app.message import context, message_builder
from app.schemas.user import UserDTO
from app.utils.bot_strings import BotStrings
from app.utils.enums.menu_type import MenuType
from app.utils.logger import setup_logger

router = Router()

logger = setup_logger(__name__)


markup_type_by_menu_type = {
    MenuType.TEACHER: MainMenuKeyboardContext(UserRole.TEACHER),
    MenuType.STUDENT: MainMenuKeyboardContext(UserRole.STUDENT),
    MenuType.ADMIN: MainMenuKeyboardContext(UserRole.ADMIN),
    MenuType.TEACHER_STUDENT: SubMenuKeyboardContext(
        UserRole.TEACHER, EntityType.STUDENT
    ),
    MenuType.TEACHER_SLOT: SubMenuKeyboardContext(UserRole.TEACHER, EntityType.SLOT),
    MenuType.TEACHER_LESSON: SubMenuKeyboardContext(
        UserRole.TEACHER, EntityType.LESSON
    ),
    MenuType.STUDENT_SLOT: SubMenuKeyboardContext(UserRole.STUDENT, EntityType.SLOT),
    MenuType.STUDENT_TEACHER: SubMenuKeyboardContext(
        UserRole.STUDENT, EntityType.TEACHER
    ),
    MenuType.ADMIN_TEMP: SubMenuKeyboardContext(UserRole.ADMIN, EntityType.UNKNOWN),
}

main_menus = [MenuType.TEACHER, MenuType.STUDENT, MenuType.ADMIN]


@router.callback_query(MenuCallback.filter(F.menu_type.in_(markup_type_by_menu_type)))
async def handle_teacher_menu(
    callback: CallbackQuery, callback_data: MenuCallback
) -> None:
    menu_type = callback_data.menu_type
    message_text = (
        BotStrings.Common.MENU
        if menu_type in main_menus
        else BotStrings.Common.SUB_MENU
    )

    message_context = context.Common(
        text=message_text, markup_context=markup_type_by_menu_type[menu_type]
    )
    await callback.message.answer(**message_builder.build(message_context))
    await callback.answer()


@router.callback_query(MenuCallback.filter(F.menu_type == MenuType.CANCEL))
async def handle_cancel(
    callback: CallbackQuery,
    state: FSMContext,
    user: UserDTO,
):
    message_context = context.Common(
        text=BotStrings.Common.MENU, markup_context=MainMenuKeyboardContext(user.role)
    )
    await state.clear()
    await callback.message.answer(**message_builder.build(message_context))
    await callback.answer()
