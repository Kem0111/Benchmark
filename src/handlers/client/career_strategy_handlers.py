from aiogram import types, Dispatcher
from core.settings import bot_messages, bot
from keyboards.career_strategy_inline_menu import (rates_keyboard,
                                                   back_to_rates_button,
                                                   back_to_strategy_button)
from .company_materials import get_career_strategy


# =================================RATES=======================================
async def get_rates(callback_query: types.CallbackQuery):
    await bot.edit_message_text(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        text=bot_messages["get_rates"],
        reply_markup=await rates_keyboard(),
        parse_mode="HTML"
    )


async def get_base_rate(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        bot_messages["get_base_rate"],
        reply_markup=await back_to_rates_button())


async def get_standart_rate(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        bot_messages["get_standart_rate"],
        reply_markup=await back_to_rates_button())


async def get_preimum_rate(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        bot_messages["get_preimum_rate"],
        reply_markup=await back_to_rates_button())


async def get_it_specialist_rate(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        bot_messages["get_it_specialist_rate"],
        reply_markup=await back_to_rates_button())


async def get_personal_rate(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        bot_messages["get_personal_rate"],
        reply_markup=await back_to_rates_button())


async def back_to_rates_handler(callback_query: types.CallbackQuery):
    await get_rates(callback_query)
# =================================RATES========================================


# =================================REVIEWS======================================
async def get_reviews(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        bot_messages["get_reviews"],
        reply_markup=await back_to_strategy_button())
# =================================REVIEWS======================================


# =================================FEEDBACK=====================================
async def get_feedback(callback_query: types.CallbackQuery):
    await bot.edit_message_text(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        text=bot_messages["get_feedback"],
        reply_markup=await back_to_strategy_button(),
        parse_mode="HTML")
# =================================FEEDBACK=====================================


# =================================FAQ==========================================
async def get_faq(callback_query: types.CallbackQuery):
    await bot.edit_message_text(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        text=bot_messages["get_faq"],
        reply_markup=await back_to_strategy_button(),
        parse_mode="HTML")
# =================================FAQ==========================================


async def back_to_strategy_handler(callback_query: types.CallbackQuery):
    await get_career_strategy(callback_query)


def register_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(
        get_rates,
        text="rates_button"
    )
    dp.register_callback_query_handler(
        back_to_strategy_handler,
        text="back_to_strategy_button"
    )
    dp.register_callback_query_handler(
        back_to_rates_handler,
        text="back_to_rates_button"
    )
    dp.register_callback_query_handler(
        get_base_rate,
        text="base_rate_button"
    )
    dp.register_callback_query_handler(
        get_standart_rate,
        text="standart_rate_button"
    )
    dp.register_callback_query_handler(
        get_preimum_rate,
        text="premium_rate_button"
    )
    dp.register_callback_query_handler(
        get_it_specialist_rate,
        text="it_specialist_rate_button"
    )
    dp.register_callback_query_handler(
        get_personal_rate,
        text="personal_rate_button"
    )
    dp.register_callback_query_handler(
        get_reviews,
        text="reviews_button"
    )
    dp.register_callback_query_handler(
        get_feedback,
        text="feedback_button"
    )
    dp.register_callback_query_handler(
        get_faq,
        text="questions_button"
    )
