from aiogram import types, Dispatcher
from core.settings import bot_messages, bot
from keyboards.begining_segmentation import (start_button,
                                             grade_buttons,
                                             menu_keyboard,
                                             set_commands)
from states.user_data import UserDataCollectionState
from aiogram.dispatcher import FSMContext


async def on_start(message: types.Message):
    bot_message = await message.answer(
        bot_messages["start"],
        reply_markup=await start_button()
    )
    return bot_message.message_id


async def start_cmd_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await state.reset_state(with_data=False)
    message_id = await on_start(message)
    await state.update_data(bot_message_ids=[message_id])


async def process_start_button(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    bot_message = await callback_query.message.answer(bot_messages["get_full_name"])
    await state.update_data(bot_message_ids=user_data['bot_message_ids'] + [bot_message.message_id])
    await state.set_state(UserDataCollectionState.WaitingForName.state)


async def get_name(message: types.Message, state: FSMContext):
    full_name = message.text
    await state.update_data(full_name=full_name)
    bot_message = await message.answer(bot_messages["get_industry"])
    user_data = await state.get_data()
    await state.update_data(bot_message_ids=user_data['bot_message_ids'] + [bot_message.message_id])
    await state.set_state(UserDataCollectionState.WaitingForIndustry.state)


async def get_industry(message: types.Message, state: FSMContext):
    industry = message.text
    await state.update_data(industry=industry)
    bot_message = await message.answer(bot_messages["get_grade"], reply_markup=await grade_buttons())
    user_data = await state.get_data()
    await state.update_data(bot_message_ids=user_data['bot_message_ids'] + [bot_message.message_id])
    await state.set_state(UserDataCollectionState.WaitingForGrade.state)


async def get_grade(callback_query: types.CallbackQuery, state: FSMContext):
    grade = callback_query.data
    user_data = await state.get_data()

    if grade == "another":
        bot_message = await callback_query.message.answer(bot_messages["get_another_grade"])
        await state.update_data(bot_message_ids=user_data['bot_message_ids'] + [bot_message.message_id])
        await state.set_state(UserDataCollectionState.WaitingForAnotherGrade.state)
    else:
        await state.update_data(grade=grade)
        bot_message = await callback_query.message.answer(bot_messages["get_source"])
        await state.update_data(bot_message_ids=user_data['bot_message_ids'] + [bot_message.message_id])
        await state.set_state(UserDataCollectionState.WaitingForSource.state)


async def get_another_grade(message: types.Message, state: FSMContext):
    grade = message.text
    await state.update_data(grade=grade)
    bot_message = await message.answer(bot_messages["get_source"])
    user_data = await state.get_data()
    await state.update_data(bot_message_ids=user_data['bot_message_ids'] + [bot_message.message_id])
    await state.set_state(UserDataCollectionState.WaitingForSource.state)


async def get_source(message: types.Message, state: FSMContext):
    source = message.text
    await state.update_data(source=source)
    bot_message = await message.answer(bot_messages["get_contact"])
    user_data = await state.get_data()
    await state.update_data(bot_message_ids=user_data['bot_message_ids'] + [bot_message.message_id])
    await state.set_state(UserDataCollectionState.WaitingForContact.state)


async def get_contact(message: types.Message, state: FSMContext):
    contact = message.text
    await state.update_data(contact=contact)
    user_data = await state.get_data()
    print(user_data)

    await message.answer(bot_messages["after_fill_form_message"], reply_markup=await menu_keyboard())
    await set_commands()

    message_ids = await state.get_data()
    for msg_id in message_ids['bot_message_ids']:
        await bot.delete_message(chat_id=message.chat.id, message_id=msg_id)

    await state.finish()
    await state.reset_state(with_data=False)


async def get_menu(message: types.Message):
    await message.answer("Выберите опцию из меню:",
                         reply_markup=await menu_keyboard())


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(
        start_cmd_handler,
        commands=['start', 'help']
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
