from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from .buttons import (
    MainMenuButtons,
    ReturnToMainMenuButtons,
)

def user_main_menu_markup() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(
            text=MainMenuButtons.ADD_URL.value,
        ),
    )

    return builder.as_markup(resize_keyboard=True)

def return_to_main_menu_markup() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(
            text=ReturnToMainMenuButtons.RETURN.value,
        ),
    )

    return builder.as_markup(resize_keyboard=True)
