from aiogram.utils.i18n import gettext as _
from aiogram.types import ReplyKeyboardMarkup

from ..maker import make_keyboard, make_button


def get_vacancy_menu_keyboard(active: bool) -> ReplyKeyboardMarkup:
    """Returns main menu keyboard."""
    return make_keyboard(
        [
            [
                make_button(
                    _("Шукаю роботу") if not active else _("Не шукаю роботу")
                )
            ],
            [
                make_button(_("Перевірити вакансії")),
                make_button(_("Отримати посилання")),
            ],
            [make_button(_("Перезеповнити анкету"))],
        ]
    )
