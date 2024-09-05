from typing import Optional

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from aiogram.client.default import DefaultBotProperties

from data.config import BOT_TOKEN

from .admins import send_to_admins
from .error import get_traceback_file_path
from .services import get_url_with_params_for_
from .decorators import optional_temp_bot_handler
from .parsing.jobs_dou import parse_dou_vacancies_from_
from .db.models import Vacancy
from .db.crud.user import delete_user_with_
from .db.crud.vacancy import get_all_active_vacancies, update_vacancy_with_


async def check_vacancies_for_all_users():
    """Checks vacancies for all users."""
    temp_bot = Bot(
        token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML")
    )
    for vacancy in get_all_active_vacancies():
        await check_vacancies_by_(vacancy, temp_bot=temp_bot)
    await temp_bot.session.close()
    del temp_bot


@optional_temp_bot_handler
async def check_vacancies_by_(
    vacancy: Vacancy, temp_bot: Optional[Bot] = None
) -> bool:
    try:
        url = get_url_with_params_for_(vacancy)
        vacancies = parse_dou_vacancies_from_(url=url)
        message_text = ""
        for vacancy_url, vacancy_data in vacancies.items():
            if vacancy_url in vacancy.last_job_urls:
                break
            message_text += (
                f"<b>{vacancy_data['date']}</b>\n"
                f"<a href='{vacancy_url}'>{vacancy_data['title']}</a> в "
                f"<a href='{vacancy_data['company']['link']}'>"
                f"{vacancy_data['company']['title']}</a>\n"
                f"<i>{vacancy_data['city']} {vacancy_data['salary']}</i>\n"
                f"{vacancy_data['description']}\n---\n"
            )
        if message_text:
            await temp_bot.send_sticker(
                vacancy.id_user_id,
                "CAACAgIAAxkBAAEMmxFmsNSE4Px-mVRRHrHYZ38dm7JNSQAC-hAAAqHHKEg5ZXbrk1gHozUE",
            )
            await temp_bot.send_message(
                vacancy.id_user_id,
                message_text[:4090],
                disable_web_page_preview=True,
            )
            update_vacancy_with_(
                user_chat_id=vacancy.id_user_id,
                last_job_urls=",".join(vacancies.keys()),
            )
            return True
    except TelegramForbiddenError:
        delete_user_with_(vacancy.id_user_id)
    except Exception as error:
        await send_to_admins(
            f"{str(error)} {str(error.__class__)[8:-2]} in checking vacancies: {url}",
            get_traceback_file_path(),
            temp_bot=temp_bot,
        )
    return False
