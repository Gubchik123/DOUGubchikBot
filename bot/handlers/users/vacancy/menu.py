from aiogram import Router
from aiogram.types import Message

from utils.db.models import Vacancy
from messages.vacancy.menu import get_vacancy_menu_message_by_


router = Router()


async def handle_vacancy_menu(message: Message, vacancy: Vacancy):
    """Handles vacancy menu."""
    await message.answer(get_vacancy_menu_message_by_(vacancy))
