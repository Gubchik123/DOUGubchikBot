import logging

from typing import Optional, Callable, Union

from aiogram import Bot
from aiogram.utils.i18n import I18n
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.client.default import DefaultBotProperties
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from data.config import BOT_TOKEN


def command_argument_required(convert: Optional[type] = str) -> Callable:
    def wrapper(command_handler: Callable) -> None:
        async def decorator(
            message: Message, scheduler: AsyncIOScheduler
        ) -> None:
            try:
                command_argument = convert(message.text.strip().split(" ")[1])
                try:
                    await command_handler(message, scheduler, command_argument)
                except TypeError:
                    await command_handler(message, command_argument)
            except IndexError:
                await message.answer("<b>Command argument is required!</b>")
            except ValueError:
                await message.answer(
                    "<b>Invalid type of the given command argument!</b> "
                    f"Expected: <i>{convert.__name__}</i>."
                )

        return decorator

    return wrapper


def before_handler_clear_state(handler: Callable) -> None:
    async def wrapper(
        event: Union[Message, CallbackQuery], state: FSMContext, i18n: I18n
    ) -> None:
        current_state = await state.get_state() if state else None

        if current_state is not None:
            logging.info(f"Cancelling state {current_state}")
            await state.clear()

        await handler(event, state, i18n)

    return wrapper


def optional_temp_bot_handler(func: Callable):
    async def wrapper(*args, **kwargs):
        temp_bot = kwargs.get("temp_bot", None)
        is_temp_bot_none = temp_bot is None

        if is_temp_bot_none:
            temp_bot = Bot(
                token=BOT_TOKEN,
                default=DefaultBotProperties(parse_mode="HTML"),
            )
            kwargs["temp_bot"] = temp_bot

        try:
            await func(*args, **kwargs)
        finally:
            if is_temp_bot_none:
                await temp_bot.session.close()
                del temp_bot

    return wrapper
