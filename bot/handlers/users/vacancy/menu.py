from random import choice

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from messages.vacancy.menu import get_vacancy_menu_message_by_
from keyboards.default.vacancy.menu import get_vacancy_menu_keyboard
from utils.decorators import vacancy_required
from utils.scheduler import check_vacancies_by_
from utils.services import get_url_with_params_for_
from utils.db.models import Vacancy
from utils.db.crud.vacancy import update_vacancy_with_, delete_vacancy_with_


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


@router.message(F.text.lower() == __("не шукаю роботу"))
@vacancy_required
async def handle_not_search_job(message: Message, vacancy: Vacancy, *args):
    """Handles the not search job button."""
    update_vacancy_with_(user_chat_id=vacancy.id_user_id, active=False)
    await handle_vacancy_menu(message, vacancy)


@router.message(F.text.lower() == __("перевірити вакансії"))
@vacancy_required
async def handle_check_vacancies(message: Message, vacancy: Vacancy, *args):
    """Handles the check vacancies button."""
    was_vacancies = await check_vacancies_by_(vacancy)
    if was_vacancies is False:
        await message.answer_sticker(
            choice(
                [
                    "CAACAgIAAxkBAAEMmw9msNROM8A5ywuyDTjoobwhmEvqCAACEg0AAtqrwUpUjHmjHVNcEjUE",
                    "CAACAgIAAxkBAAEMm9JmsguptxkU2xwf3g7mW-JKvuR67gACPQ0AAu7hYEki8vUJecaK4DUE",
                    "CAACAgIAAxkBAAEMm9BmsgtD1ihaAAFK_SexzLlE3XeXnZIAAlUMAAJTN1lJ7r4gyMng9Eg1BA",
                ]
            )
        )
        await message.answer(_("Нових вакансій не знайдено!"))


@router.message(F.text.lower() == __("отримати посилання"))
@vacancy_required
async def handle_get_link(message: Message, vacancy: Vacancy, *args):
    """Handles the get link button."""
    await message.answer_sticker(
        "CAACAgIAAxkBAAEMm9Rmsgut4PnLYYm0JJctuVxqfVr8OwACoQ4AAgkouErdJlk-PMSKuDUE"
    )
    await message.answer(get_url_with_params_for_(vacancy))


@router.message(F.text.lower() == __("перезаповнити анкету"))
@vacancy_required
async def handle_restart_vacancy_quiz(
    message: Message, vacancy: Vacancy, state: FSMContext
):
    """Handles the restart vacancy quiz button."""
    from .quiz import start_vacancy_quiz

    delete_vacancy_with_(user_chat_id=vacancy.id_user_id)
    await start_vacancy_quiz(message, state)
