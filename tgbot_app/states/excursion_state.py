from aiogram.dispatcher.filters.state import State, StatesGroup


class ExcursionState(StatesGroup):
    country = State()
    city = State()
