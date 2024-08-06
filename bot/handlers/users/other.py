from aiogram import Router
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from aiogram.exceptions import TelegramBadRequest


router = Router()


@router.message()
async def handle_all_other_messages(message: Message):
    """Handles all other messages."""
    try:
        await message.answer(
            _(
                "Я Вас не розумію :(\n"
                "Раджу використати кнопки або команди для задуманого результату."
            )
        )
    except TelegramBadRequest:
        pass
