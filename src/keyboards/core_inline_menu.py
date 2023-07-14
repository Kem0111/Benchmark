from aiogram.types import (InlineKeyboardMarkup,
                           InlineKeyboardButton)

from core.settings import bot_messages


async def b2b_b2c_buttons():
    keyboard = InlineKeyboardMarkup(row_width=1)

    buttons = [
        InlineKeyboardButton(bot_messages["b2b_button"],
                             callback_data="b2b_button"),
        InlineKeyboardButton(bot_messages["b2c_button"],
                             callback_data="b2c_button"),
        InlineKeyboardButton(bot_messages["back"],
                             callback_data="back_to_menu")
    ]
    keyboard.add(*buttons)
    return keyboard


async def career_strategy_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)

    buttons = [
        InlineKeyboardButton(bot_messages["rates_button"],
                             callback_data="rates_button"),
        InlineKeyboardButton(bot_messages["reviews_button"],
                             callback_data="reviews_button"),
        InlineKeyboardButton(bot_messages["feedback_button"],
                             callback_data="feedback_button"),
        InlineKeyboardButton(bot_messages["questions_button"],
                             callback_data="questions_button"),
        InlineKeyboardButton(bot_messages["back"],
                             callback_data="back_to_menu")
    ]
    keyboard.add(*buttons)
    return keyboard


async def back_to_menu():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(bot_messages["back"],
                                      callback_data="back_to_menu"))
    return keyboard
