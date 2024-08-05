import logging
from typing import Optional

from aiogram import Bot
from aiogram.types import FSInputFile

from data.config import ADMINS

from .decorators import optional_temp_bot_handler


async def notify_admins_on_startup_of_(bot: Bot) -> None:
    """Notifies admins on bot startup."""
    for admin in ADMINS:
        try:
            await bot.send_message(admin, "Bot started!")
        except Exception as err:
            logging.exception(err)


@optional_temp_bot_handler
async def send_to_admins(*messages: str, temp_bot: Optional[Bot] = None):
    """Sends the given message to all admins"""
    for admin_chat_id in ADMINS:
        for message in messages:
            if message.endswith(".txt"):
                await temp_bot.send_document(
                    admin_chat_id, document=FSInputFile(message)
                )
            else:
                await temp_bot.send_message(admin_chat_id, text=message)
