from aiogram import types
from aiogram.types import (InlineKeyboardMarkup,
                           InlineKeyboardButton)

from bot.src.core.settings import bot_messages, bot


async def start_button():
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(bot_messages["start_button"],
                             callback_data="start_button"),
        InlineKeyboardButton(bot_messages["security"],
                             url="https://benchmark.ru.com/privacy"),
    ]
    keyboard.add(*buttons)
    return keyboard


async def grade_buttons():
    keyboard = InlineKeyboardMarkup(row_width=1)

    grade_button_1 = InlineKeyboardButton(bot_messages["middle_button"],
                                          callback_data="Middle")
    grade_button_2 = InlineKeyboardButton(bot_messages["senior_button"],
                                          callback_data="Senior")
    grade_button_3 = InlineKeyboardButton(
        bot_messages["top_management_button"],
        callback_data="Top-management")

    grade_button_4 = InlineKeyboardButton(
        bot_messages["another_button"],
        callback_data="another")

    keyboard.add(grade_button_1, grade_button_2,
                 grade_button_3, grade_button_4)
    return keyboard


async def menu_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(
            bot_messages["who_is_us_button"],
            callback_data="who_is_us_button"
        ),
        InlineKeyboardButton(
            bot_messages["for_candidate_btn"],
            callback_data="for_candidate_btn"
        ),
        InlineKeyboardButton(
            bot_messages["for_company_btn"],
            callback_data="for_company_btn"
        ),
        InlineKeyboardButton(
            bot_messages["connect_with_us_button"],
            url="https://benchmark.ru.com/telegram_form"
        ),
    ]
    keyboard.add(*buttons)
    return keyboard


async def for_candidate_kb():
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(
                bot_messages["career_strategy_button"],
                callback_data="career_strategy_button"
            ),
        InlineKeyboardButton(
            bot_messages["usefull_materials_button"],
            callback_data="usefull_materials_button"
        ),
        InlineKeyboardButton(
            bot_messages["open_vacancy_button"],
            url="https://benchmark.zohorecruit.com/jobs"
        ),
        InlineKeyboardButton(bot_messages["back"],
                             callback_data="back_to_menu")
    ]
    keyboard.add(*buttons)
    return keyboard


async def for_company_kb():
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(
            bot_messages["products_button"],
            callback_data="products_button"
        ),
        InlineKeyboardButton(bot_messages["back"],
                             callback_data="back_to_menu")
    ]
    keyboard.add(*buttons)
    return keyboard


async def set_commands():
    commands = [
        types.MenuButton(command="/start", description="Начать"),
    ]

    await bot.set_my_commands(commands=commands)
