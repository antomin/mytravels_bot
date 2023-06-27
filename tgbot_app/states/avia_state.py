from aiogram.dispatcher.filters.state import StatesGroup, State


class AviaState(StatesGroup):
    target = State()
    depart = State()
    arrival = State()
    date_depart = State()
    date_return = State()
    is_direct = State()
