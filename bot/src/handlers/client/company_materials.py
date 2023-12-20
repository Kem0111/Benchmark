from aiogram import types, Dispatcher
from bot.src.core.settings import bot_messages, bot
from bot.src.keyboards.core_inline_menu import (b2b_b2c_buttons,
                                                career_strategy_keyboard,
                                                back_to_menu)
from bot.src.keyboards.begining_segmentation import (
    for_candidate_kb, for_company_kb, menu_keyboard
)


async def get_company_info(callback_query: types.CallbackQuery):

    await bot.edit_message_text(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        text=bot_messages["get_company_info"],
        parse_mode='HTML',
        reply_markup=await b2b_b2c_buttons()
    )


async def get_career_strategy(callback_query: types.CallbackQuery):
    await bot.edit_message_text(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        text=bot_messages["get_career_strategy"],
        reply_markup=await career_strategy_keyboard()
    )


async def get_usefull_materials(callback_query: types.CallbackQuery):
    await bot.edit_message_text(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        text=bot_messages["get_usefull_materials"],
        reply_markup=await back_to_menu('for_candidate_btn'),
        parse_mode="HTML",
    )


async def back_to_menu_handler(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text("Выберите опцию из меню:",
                                           reply_markup=await menu_keyboard())


async def for_candidate_handler(callback_query: types.CallbackQuery):
    await callback_query.message.edit_reply_markup(
        reply_markup=await for_candidate_kb()
    )


async def for_company_handler(callback_query: types.CallbackQuery):
    await bot.edit_message_text(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        text=bot_messages["get_products"],
        parse_mode="HTML",
        reply_markup=await back_to_menu("back_to_menu")
     )


def register_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(
        get_company_info,
        text="who_is_us_button"
    )
    dp.register_callback_query_handler(
        get_career_strategy,
        text="career_strategy_button"
    )
    dp.register_callback_query_handler(
        for_candidate_handler,
        text="for_candidate_btn"
    )
    dp.register_callback_query_handler(
        for_company_handler,
        text="for_company_btn"
    )
    dp.register_callback_query_handler(
        get_usefull_materials,
        text="usefull_materials_button"
    )
    dp.register_callback_query_handler(
        back_to_menu_handler,
        text="back_to_menu"
    )
