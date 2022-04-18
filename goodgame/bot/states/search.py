from aiogram.dispatcher.filters.state import State, StatesGroup


class SearchState(StatesGroup):
    SELECT_CATEGORY = State()
    SELECT_GAME = State()
    SEARCH = State()