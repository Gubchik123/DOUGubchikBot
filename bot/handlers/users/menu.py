from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from utils.db.crud.vacancy import get_vacancy_by_

from .vacancy.quiz import start_vacancy_quiz
from .vacancy.menu import handle_vacancy_menu


router = Router()


async def handle_menu(message: Message, state: FSMContext):
    """Handles main menu."""
    vacancy = get_vacancy_by_(message.from_user.id)
    if vacancy:
        await handle_vacancy_menu(message, vacancy)
    else:
        await start_vacancy_quiz(message, state)
