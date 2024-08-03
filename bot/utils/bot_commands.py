from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats


async def set_default_commands_for_(bot: Bot) -> None:
    """Sets default bot commands for uk and en languages."""
    bot_commands = {
        "uk": [
            BotCommand(command="start", description="Початок роботи з ботом"),
            BotCommand(
                command="help",
                description="Отримати основні правила використання",
            ),
            BotCommand(command="menu", description="Отримати головне меню"),
        ],
        "en": [
            BotCommand(
                command="start", description="Start working with the bot"
            ),
            BotCommand(command="help", description="Get basic usage rules"),
            BotCommand(command="menu", description="Get main menu"),
        ],
    }
    for language_code, commands in bot_commands.items():
        await bot.set_my_commands(
            commands=commands,
            scope=BotCommandScopeAllPrivateChats(),
            language_code=language_code,
        )
