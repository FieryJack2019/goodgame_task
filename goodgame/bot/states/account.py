from aiogram.dispatcher.filters.state import State, StatesGroup


class AccountRegisterState(StatesGroup):
    SELECT_CATEGORY = State()
    SELECT_GAME = State()
    INPUT_STEAM = State()
    INPUT_ABOUT = State()


class AccountEditState(StatesGroup):
    SELECT_FIELD = State()
    EDIT_FIELD = State()
    EDIT_CATEGORY = State()
    EDIT_GAME = State()