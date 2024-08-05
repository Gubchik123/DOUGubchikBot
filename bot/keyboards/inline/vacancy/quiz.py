from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.constants import CATEGORIES, EXPERIENCE, CITIES

from ..maker import make_inline_keyboard_builder_for_list_of_


def get_categories_inline_keyboard() -> InlineKeyboardMarkup:
    """Returns an inline keyboard with categories."""
    return make_inline_keyboard_builder_for_list_of_(
        CATEGORIES, 3, "category"
    ).as_markup()


def get_cities_inline_keyboard() -> InlineKeyboardMarkup:
    """Returns an inline keyboard with cities."""
    callback = "city"
    inline_keyboard_builder = make_inline_keyboard_builder_for_list_of_(
        CITIES, 3, callback
    )
    inline_keyboard_builder.row(
        InlineKeyboardButton(
            text=_("Віддалена робота"),
            callback_data=f"btn_{callback}:remote",
        )
    )
    inline_keyboard_builder.row(
        InlineKeyboardButton(
            text=_("За кордоном"),
            callback_data=f"btn_{callback}:relocate",
        )
    )
    return inline_keyboard_builder.as_markup()


def get_experience_inline_keyboard() -> InlineKeyboardMarkup:
    """Returns an inline keyboard with experience."""
    # TODO: make_inline_keyboard_builder_for_dict_of_ if will be one more dict like EXPERIENCE
    inline_keyboard_builder = InlineKeyboardBuilder()
    for index, (button, callback) in enumerate(EXPERIENCE.items()):
        keyboard_add_method = (
            inline_keyboard_builder.add
            if index % 2
            else inline_keyboard_builder.row
        )
        keyboard_add_method(
            InlineKeyboardButton(
                text=button,
                callback_data=f"btn_experience:{callback}",
            )
        )
    return inline_keyboard_builder.as_markup()
