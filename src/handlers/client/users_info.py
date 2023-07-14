from aiogram import types, Dispatcher
from core.settings import bot_messages
from keyboards.begining_segmentation import (start_button,
                                             grade_buttons,
                                             menu_keyboard,
                                             set_commands)
from states.user_data import UserDataCollectionState
from aiogram.dispatcher import FSMContext


async def on_start(message: types.Message):
    await message.answer(
        bot_messages["start"],
        reply_markup=await start_button()
    )


async def start_cmd_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await state.reset_state(with_data=False)
    await on_start(message)


async def process_start_button(callback_query: types.CallbackQuery,
                               state: FSMContext):

    await callback_query.message.answer(
        bot_messages["get_full_name"]
    )
    await state.set_state(UserDataCollectionState.WaitingForName.state)


async def get_name(message: types.Message, state: FSMContext):
    full_name = message.text
    await state.update_data(full_name=full_name)
    await message.answer(bot_messages["get_industry"])
    await state.set_state(UserDataCollectionState.WaitingForIndustry.state)


async def get_industry(message: types.Message, state: FSMContext):
    industry = message.text
    await state.update_data(industry=industry)
    await message.answer(
        bot_messages["get_grade"],
        reply_markup=await grade_buttons()
    )
    await state.set_state(UserDataCollectionState.WaitingForGrade.state)


async def get_grade(callback_query: types.CallbackQuery, state: FSMContext):
    grade = callback_query.data

    if grade == "another":
        await callback_query.message.answer(bot_messages["get_another_grade"])
        await state.set_state(
            UserDataCollectionState.WaitingForAnotherGrade.state
        )
    else:
        await state.update_data(grade=grade)
        await callback_query.message.answer(bot_messages["get_source"])
        await state.set_state(UserDataCollectionState.WaitingForSource.state)


async def get_another_grade(message: types.Message, state: FSMContext):
    grade = message.text
    await state.update_data(grade=grade)
    await message.answer(bot_messages["get_source"])
    await state.set_state(UserDataCollectionState.WaitingForSource.state)


async def get_source(message: types.Message, state: FSMContext):
    source = message.text
    await state.update_data(source=source)
    await message.answer(bot_messages["get_contact"])
    await state.set_state(UserDataCollectionState.WaitingForContact.state)


async def get_contact(message: types.Message, state: FSMContext):
    contact = message.text
    await state.update_data(contact=contact)
    user_data = await state.get_data()
    print(user_data)

    await message.answer(bot_messages["after_fill_form_message"],
                         reply_markup=await menu_keyboard())

    await set_commands()
    await state.finish()


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
