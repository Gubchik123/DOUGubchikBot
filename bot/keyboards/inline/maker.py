from typing import Optional

from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def make_inline_keyboard_builder_for_list_of_(
    lst: list, btns_per_row: int, callback: str
) -> InlineKeyboardBuilder:
    """Returns an inline keyboard builder with items from the given list."""
    inline_keyboard_builder = InlineKeyboardBuilder()
    for index, item in enumerate(lst):
        keyboard_add_method = (
            inline_keyboard_builder.add
            if index % btns_per_row
            else inline_keyboard_builder.row
        )
        keyboard_add_method(
            InlineKeyboardButton(
                text=item,
                callback_data=f"btn_{callback}:{item}",
            )
        )
    return inline_keyboard_builder


def make_yes_or_no_inline_keyboard(
    yes_callback_data: str,
    no_callback_data: str,
    yes_btn_text: Optional[str] = None,
    no_btn_text: Optional[str] = None,
) -> InlineKeyboardMarkup:
    """Returns made inline keyboard with (yes) and (no) buttons."""
    return (
        InlineKeyboardBuilder()
        .add(
            InlineKeyboardButton(
                text=yes_btn_text or _("Так"), callback_data=yes_callback_data
            ),
            InlineKeyboardButton(
                text=no_btn_text or _("Ні"), callback_data=no_callback_data
            ),
        )
        .as_markup()
    )
