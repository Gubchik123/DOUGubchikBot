from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.i18n import lazy_gettext as __

from utils.decorators import vacancy_required
from utils.db.models import Vacancy
from utils.db.crud.vacancy import update_vacancy_with_
from messages.vacancy.menu import get_vacancy_menu_message_by_
from keyboards.default.vacancy.menu import get_vacancy_menu_keyboard


router = Router()


async def handle_vacancy_menu(message: Message, vacancy: Vacancy):
    """Handles vacancy menu."""
    await message.answer(
        get_vacancy_menu_message_by_(vacancy),
        reply_markup=get_vacancy_menu_keyboard(vacancy.active),
    )


@router.message(F.text.lower() == __("шукаю роботу"))
@vacancy_required
async def handle_search_job(message: Message, vacancy: Vacancy, *args):
    """Handles the search job button."""
    update_vacancy_with_(user_chat_id=vacancy.id_user_id, active=True)
    await handle_vacancy_menu(message, vacancy)
