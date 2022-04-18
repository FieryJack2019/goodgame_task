from aiogram.dispatcher.filters.state import State, StatesGroup


class MenuState(StatesGroup):
    MENU = State()
    PROFILE = State()