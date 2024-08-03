from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from aiogram.client.default import DefaultBotProperties

from data.config import BOT_TOKEN

from .admins import send_to_admins
from .db.crud.user import get_user_by_, delete_user_with_
from .error import (
    get_admin_error_message,
    get_traceback_file_path,
    get_user_error_message,
)
