import asyncio

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.utils.i18n import gettext as _
from sqlalchemy.exc import IntegrityError

from data.config import ADMINS
from utils.admins import send_to_admins
from utils.db.crud.user import create_user_by_
from utils.decorators import before_handler_clear_state

from ..menu import handle_menu


router = Router()


@router.message(CommandStart())
@before_handler_clear_state
async def handle_start_command(message: Message, *args):
    """Handles the /start command.
    Creates a new user in the database if it does not exist."""
    try:
        user = message.from_user
        create_user_by_(user)
        await _greet_user(message, user.full_name)
        if user.id not in ADMINS:
            asyncio.create_task(
                send_to_admins(
                    f"🆕👤 {user.full_name} (<code>{user.id}</code>)."
                )
            )
    except IntegrityError:  # psycopg2.errors.UniqueViolation
        await _greet_user(message, message.from_user.full_name)


async def _greet_user(message: Message, user_full_name: str):
    """Sends a greeting message to the user."""
    await message.answer_sticker(
        "CAACAgIAAxkBAAEMmOVmriQu5yzwLBHbT9bTPmA3zJCqcQACjg8AAg3GCEprgFmiFwjklzUE"
    )
    await message.answer(
        _(
            "Привіт, {name}!\n"
            "Я той, хто допоможе Вам відстежувати нові вакансії на сайті dou.ua"
        ).format(name=user_full_name)
    )
    await handle_menu(message)
