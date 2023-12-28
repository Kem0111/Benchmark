from aiogram.types import (InlineKeyboardMarkup,
                           InlineKeyboardButton)

from bot.src.core.settings import bot_messages


async def b2b_b2c_buttons():
    keyboard = InlineKeyboardMarkup(row_width=1)

    buttons = [
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
                             url="https://drive.google.com/file/d/1gmpmgojFoM95tjGsL3FkHECc_f5cHish/view?usp=sharing"),
        InlineKeyboardButton(bot_messages["feedback_button"],
                             callback_data="feedback_button"),
        InlineKeyboardButton(bot_messages["consultation_button"],
                             url="https://benchmark.ru.com/career_strategy"),
        InlineKeyboardButton(bot_messages["back"],
                             callback_data="for_candidate_btn")
    ]
    keyboard.add(*buttons)
    return keyboard


async def back_to_menu(back_call):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(bot_messages["back"],
                                      callback_data=back_call))
    return keyboard
