from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.i18n import gettext as _

from utils.decorators import before_handler_clear_state


router = Router()


@router.message(Command("help"))
@before_handler_clear_state
async def handle_help_command(message: Message, *args):
    """Handles the /help command."""
    await message.answer(
        _(
            "Команди бота:\n"
            "/start - Початок роботи з ботом\n"
            "/help - Отримати основні правила використання\n"
            "/menu - Отримати головне меню\n\n"
            "Раджу використати кнопки для задуманого результату\n\n"
            "Приємного використання!!!\n\n"
            "Запропонувати ідею або виявити помилку можна за посиланням:\n"
            "https://github.com/Gubchik123/DouGubchikBot/issues/new\n\n"
            "Контакти автора бота:\n"
            "Сайт резюме: https://hubariev.com\n"
            "LinkedIn: https://www.linkedin.com/in/nikita-hubariev\n"
            "Instagram: https://www.instagram.com/notwhale.1746\n\n"
            "Інші проекти автора доступні на:\n"
            "Портфоліо: https://portfolio.hubariev.com\n"
            "GitHub: https://github.com/Gubchik123\n"
        )
    )
