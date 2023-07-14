from aiogram.dispatcher.filters.state import StatesGroup, State


class UserDataCollectionState(StatesGroup):
    WaitingForName = State()
    WaitingForIndustry = State()
    WaitingForGrade = State()
    WaitingForSource = State()
    WaitingForContact = State()
    WaitingForAnotherGrade = State()
