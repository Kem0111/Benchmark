from aiogram.types import (InlineKeyboardMarkup,
                           InlineKeyboardButton)
from bot.src.core.settings import bot_messages


async def rates_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)

    buttons = [
        InlineKeyboardButton(bot_messages["base_rate_button"],
                             callback_data="base_rate_button"),
        InlineKeyboardButton(bot_messages["standart_rate_button"],
                             callback_data="standart_rate_button"),
        InlineKeyboardButton(bot_messages["premium_rate_button"],
                             callback_data="premium_rate_button"),
        InlineKeyboardButton(bot_messages["it_specialist_rate_button"],
                             callback_data="it_specialist_rate_button"),
        InlineKeyboardButton(bot_messages["back"],
                             callback_data="back_to_strategy_button")
    ]
    keyboard.add(*buttons)
    return keyboard


async def back_to_strategy_button():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(bot_messages["back"],
                                      callback_data="back_to_strategy_button"))
    return keyboard


async def back_to_rates_button():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(bot_messages["back"],
                                      callback_data="back_to_rates_button"))
    return keyboard
