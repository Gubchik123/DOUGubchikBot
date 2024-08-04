from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from filters.is_admin import IsAdmin
from utils.db.crud.vacancy import get_vacancy_by_
from utils.decorators import command_argument_required


router = Router()


@router.message(IsAdmin(), Command("vacancy"))
@command_argument_required(int)
async def handle_vacancy_command(message: Message, user_chat_id: int) -> None:
    """Handles the /vacancy command."""
    if (vacancy := get_vacancy_by_(user_chat_id)) is None:
        await message.answer("<i>Vacancy not found.</i>")
        return
    await message.answer(
        f"🆔 <code>{vacancy.id_user_id}</code>\n"
        f"🔛 active {vacancy.active}\n"
        f"🔗 jobs.dou.ua / {vacancy.url_prefix}\n\n"
        f"🏷 {vacancy.category}\n"
        f"📅 {vacancy.exp}\n"
        f"🏙 {vacancy.city}\n"
        f"🌐 remote {vacancy.remote}\n"
        f"🚚 relocate {vacancy.relocate}\n"
        f"📝 descr {vacancy.descr}\n"
        f"🔍 search = {vacancy.search}\n"
    )
