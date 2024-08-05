from aiogram import Router
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from utils.db.models import Vacancy


router = Router()


async def handle_vacancy_menu(message: Message, vacancy: Vacancy):
    """Handles vacancy menu."""
    await message.answer(
        _(
            "<b>Меню пошуку</b>\n\n"
            "Шукаєте роботу зараз? {vacancy.active}\n\n"
            "Категорія: {vacancy.category}\n"
            "Досвід: {vacancy.exp}\n"
            "Місто: {vacancy.city}\n\n"
            "Віддалена робота? {vacancy.remote}\n"
            "За кордоном? {vacancy.relocate}\n"
            "Пошуковий запит: {vacancy.search}\n"
            "Шукати в описі вакансій? {vacancy.descr}\n"
        ).format(vacancy=vacancy)
    )
