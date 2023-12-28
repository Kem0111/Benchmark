from aiogram import types, Dispatcher
from bot.src.core.settings import bot_messages, bot
from bot.src.keyboards.begining_segmentation import (start_button,
                                                     grade_buttons,
                                                     menu_keyboard,
                                                     set_commands)
from bot.src.states.user_data import UserDataCollectionState
from aiogram.dispatcher import FSMContext
from bot.models import TelegramUser, Profile
import re
from bot.src.core.http_client import zoho_client


async def update_bot_message_ids(state: FSMContext,
                                 bot_message: types.Message):

    await state.update_data(
        bot_message_id=bot_message.message_id
    )


async def delete_prev_bot_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    msg_id = data.get('bot_message_id')
    if msg_id:
        await bot.delete_message(chat_id=message.chat.id, message_id=msg_id)


# =================================HANDLERS=====================================
async def on_start(message: types.Message):
    bot_message = await message.answer(
        bot_messages["start"],
        reply_markup=await start_button()
    )
    return bot_message.message_id


async def start_cmd_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await state.reset_data()
    await set_commands()
    user = await TelegramUser.objects.filter(
        tg_id=message.from_user.id
    ).afirst()

    if user:
        await get_menu(message)
    else:
        await delete_prev_bot_message(message, state)
        await state.finish()
        await state.reset_state(with_data=True)
        message_id = await on_start(message)
        await state.update_data(bot_message_id=message_id)


async def process_start_button(callback_query: types.CallbackQuery, state: FSMContext):
    await delete_prev_bot_message(callback_query.message, state)
    bot_message = await callback_query.message.answer(bot_messages["get_full_name"])
    await update_bot_message_ids(state, bot_message)

    await state.set_state(UserDataCollectionState.WaitingForName.state)


async def get_name(message: types.Message, state: FSMContext):
    await delete_prev_bot_message(message, state)
    full_name = message.text
    await state.update_data(
        Last_Name=full_name,
        Lead_Status='New',
        Lead_Source='Telegram'
    )
    bot_message = await message.answer(bot_messages["get_industry"])
    await update_bot_message_ids(state, bot_message)
    await state.set_state(UserDataCollectionState.WaitingForIndustry.state)
    await message.delete()


async def get_industry(message: types.Message, state: FSMContext):
    await delete_prev_bot_message(message, state)
    industry = message.text
    await state.update_data(Industry=industry)
    bot_message = await message.answer(bot_messages["get_grade"],
                                       reply_markup=await grade_buttons())
    await update_bot_message_ids(state, bot_message)
    await state.set_state(UserDataCollectionState.WaitingForGrade.state)
    await message.delete()


async def get_grade(callback_query: types.CallbackQuery, state: FSMContext):
    grade = callback_query.data
    await delete_prev_bot_message(callback_query.message, state)
    if grade == "another":
        bot_message = await callback_query.message.answer(
            bot_messages["get_another_grade"]
        )
        await update_bot_message_ids(state, bot_message)
        await state.set_state(UserDataCollectionState.WaitingForAnotherGrade.state)
    else:
        await state.update_data(grade=grade)
        bot_message = await callback_query.message.answer(bot_messages["get_source"])
        await update_bot_message_ids(state, bot_message)
        await state.set_state(UserDataCollectionState.WaitingForSource.state)


async def get_another_grade(message: types.Message, state: FSMContext):
    await delete_prev_bot_message(message, state)
    grade = message.text
    await state.update_data(grade=grade)
    bot_message = await message.answer(bot_messages["get_source"])
    await update_bot_message_ids(state, bot_message)
    await state.set_state(UserDataCollectionState.WaitingForSource.state)
    await message.delete()


async def get_source(message: types.Message, state: FSMContext):
    await delete_prev_bot_message(message, state)
    source = message.text
    await state.update_data(Description=source)
    bot_message = await message.answer(bot_messages["get_contact"])
    await update_bot_message_ids(state, bot_message)
    await state.set_state(UserDataCollectionState.WaitingForContact.state)
    await message.delete()


def is_phone_number(number):
    phone_regex = r'(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){10,14}(\s*)?'

    return re.match(phone_regex, number)


async def get_contact(message: types.Message, state: FSMContext):
    await delete_prev_bot_message(message, state)
    contact = message.text
    if is_phone_number(contact):
        await state.update_data(Phone=contact)
    else:
        await state.update_data(Email=contact)
    lead_data = await state.get_data()
    lead_data.pop('bot_message_id')
    grade = lead_data.pop('grade')
    lead_data['Industry'] = f"{lead_data['Industry']} {grade}"
    # await zoho_client.send_lead(lead_data)

    await TelegramUser.objects.acreate(
        tg_id=message.from_user.id,
        user_name=message.from_user.username
    )
    try:
        await Profile.objects.acreate(
            user_id=message.from_user.id,
            full_name=lead_data.get('Last_Name', ''),
            industry=lead_data.get('Industry', ''),
            grade=grade,
            source=lead_data.get('Description', ''),
            contact=lead_data.get('Phone', '') or lead_data.get('Email', '')
        )
    except Exception as e:
        print(e)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=bot_messages["after_fill_form_message"],
        reply_markup=await menu_keyboard(),
        parse_mode='HTML'
    )

    await state.finish()
    await state.reset_state(with_data=False)
    await state.update_data(completed_survey=True)
    await message.delete()


async def get_menu(message: types.Message):
    await message.answer("Выберите опцию из меню:", reply_markup=await menu_keyboard())


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(
        start_cmd_handler,
        commands=['start', 'help'],
        state="*"
    )
    dp.register_callback_query_handler(
        process_start_button,
        lambda c: c.data.startswith("start_button")
    )
    dp.register_callback_query_handler(
        get_grade,
        state=UserDataCollectionState.WaitingForGrade
    )
    dp.register_message_handler(
        get_another_grade,
        state=UserDataCollectionState.WaitingForAnotherGrade
    )
    dp.register_message_handler(
        get_industry,
        state=UserDataCollectionState.WaitingForIndustry
    )
    dp.register_message_handler(
        get_name,
        state=UserDataCollectionState.WaitingForName
    )
    dp.register_message_handler(
        get_source,
        state=UserDataCollectionState.WaitingForSource
    )
    dp.register_message_handler(
        get_contact,
        state=UserDataCollectionState.WaitingForContact
    )
    dp.register_message_handler(
        get_menu,
        commands=['who_are_we']
    )
