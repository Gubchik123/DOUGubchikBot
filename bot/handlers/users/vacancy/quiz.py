import asyncio

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from aiogram.types import Message, CallbackQuery

from data.config import ADMINS
from utils.admins import send_to_admins
from states.vacancy_quiz import VacancyQuiz
from utils.db.crud.vacancy import create_vacancy_for_
from keyboards.inline.vacancy import quiz as quiz_kb
from keyboards.inline.maker import make_yes_or_no_inline_keyboard

from .menu import handle_vacancy_menu


router = Router()


async def start_vacancy_quiz(message: Message, state: FSMContext):
    """Starts vacancy quiz."""
    await message.answer(
        _("Оберіть категорію вакансії:"),
        reply_markup=quiz_kb.get_categories_inline_keyboard(),
    )
    await state.set_state(VacancyQuiz.category)


@router.callback_query(F.data.startswith("btn_category"), VacancyQuiz.category)
async def handle_category(callback_query: CallbackQuery, state: FSMContext):
    """Handles the category of the vacancy."""
    category = callback_query.data.split(":")[-1]
    await state.update_data(category=category)
    await _ask_about_experience(callback_query, state)


async def _ask_about_experience(
    callback_query: CallbackQuery, state: FSMContext
):
    """Asks about the work experience."""
    await callback_query.message.edit_text(
        _("Який у вас досвід роботи?"),
        reply_markup=quiz_kb.get_experience_inline_keyboard(),
    )
    await state.set_state(VacancyQuiz.exp)


@router.callback_query(F.data.startswith("btn_experience"), VacancyQuiz.exp)
async def handle_experience(callback_query: CallbackQuery, state: FSMContext):
    """Handles the work experience."""
    exp = callback_query.data.split(":")[-1]
    url_prefix = "vacancies"
    if exp == "-":
        exp = None
        url_prefix = "first-job"
    await state.update_data(exp=exp, url_prefix=url_prefix)
    await _ask_about_city(callback_query, state)


async def _ask_about_city(callback_query: CallbackQuery, state: FSMContext):
    """Asks about the city."""
    await callback_query.message.edit_text(
        _("У якому місті ви шукаєте роботу?"),
        reply_markup=quiz_kb.get_cities_inline_keyboard(),
    )
    await state.set_state(VacancyQuiz.city)


@router.callback_query(F.data.startswith("btn_city"), VacancyQuiz.city)
async def handle_city(callback_query: CallbackQuery, state: FSMContext):
    """Handles the city."""
    city = callback_query.data.split(":")[-1]
    remote = False
    relocate = False
    if city == "remote":
        remote = True
        city = None
    elif city == "relocate":
        relocate = True
        city = None
    await state.update_data(city=city, remote=remote, relocate=relocate)
    await _ask_about_search(callback_query, state)


async def _ask_about_search(callback_query: CallbackQuery, state: FSMContext):
    """Asks about the search."""
    await callback_query.message.edit_text(
        _(
            "Чи бажаєте Ви розширити пошук своїм пошуковим запитом? "
            "Наприклад, Python Kharkiv"
        ),
        reply_markup=make_yes_or_no_inline_keyboard(
            yes_callback_data="btn_yes_search",
            no_callback_data="btn_no_search",
        ),
    )
    await state.set_state(VacancyQuiz.is_search)


@router.callback_query(F.data == "btn_yes_search", VacancyQuiz.is_search)
async def ask_search_query(callback_query: CallbackQuery, state: FSMContext):
    """Asks about the search query."""
    await callback_query.message.edit_text(
        _(
            "Введіть пошуковий запит.\n\nПосада, мова, компанія, місто, країна. "
            "Наприклад, Python Kharkiv"
        ),
    )
    await state.set_state(VacancyQuiz.search)


@router.message(VacancyQuiz.search)
async def handle_search_query(message: Message, state: FSMContext):
    """Handles the search query."""
    await state.update_data(search=message.text)
    await _ask_about_descr(message, state)


async def _ask_about_descr(message: Message, state: FSMContext):
    """Asks about searching in the description."""
    await message.answer(
        _("Чи бажаєте Ви шукати в описах вакансій?"),
        reply_markup=make_yes_or_no_inline_keyboard(
            yes_callback_data="btn_descr:1", no_callback_data="btn_descr:0"
        ),
    )
    await state.set_state(VacancyQuiz.descr)


@router.callback_query(F.data.startswith("btn_descr"), VacancyQuiz.descr)
async def handle_descr(callback_query: CallbackQuery, state: FSMContext):
    """Handles searching in the description."""
    await state.update_data(
        descr=bool(int(callback_query.data.split(":")[-1]))
    )
    await ask_about_active(callback_query, state)


@router.callback_query(F.data == "btn_no_search", VacancyQuiz.is_search)
async def ask_about_active(callback_query: CallbackQuery, state: FSMContext):
    """Asks about the current search status."""
    await callback_query.message.edit_text(
        _("Ви наразі шукаєте роботу за цими критеріями?"),
        reply_markup=make_yes_or_no_inline_keyboard(
            yes_callback_data="btn_active:1", no_callback_data="btn_active:0"
        ),
    )
    await state.set_state(VacancyQuiz.active)


@router.callback_query(F.data.startswith("btn_active"), VacancyQuiz.active)
async def handle_active(callback_query: CallbackQuery, state: FSMContext):
    """Handles the current search status."""
    await state.update_data(
        active=bool(int(callback_query.data.split(":")[-1]))
    )
    await _finish_vacancy_quiz(callback_query, state)


async def _finish_vacancy_quiz(
    callback_query: CallbackQuery, state: FSMContext
):
    """Finishes the vacancy quiz."""
    user = callback_query.from_user
    data = await state.get_data()
    vacancy = create_vacancy_for_(user_chat_id=user.id, state_data=data)
    await state.clear()

    await callback_query.message.edit_text(
        _("Ви успішно заповнили пошукові дані для вакансій!")
    )
    await handle_vacancy_menu(callback_query.message, vacancy)

    if user.id not in ADMINS:
        asyncio.create_task(
            send_to_admins(
                f"🆕🔍 {user.full_name} (<code>{user.id}</code>) "
                f"filled out the vacancy quiz."
            )
        )
