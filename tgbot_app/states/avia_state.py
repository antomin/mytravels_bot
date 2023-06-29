from aiogram.dispatcher.filters.state import State, StatesGroup


class AviaState(StatesGroup):
    target = State()
    depart_country = State()
    depart_city = State()
    arrival_country = State()
    arrival_city = State()
    date_depart = State()
    date_return = State()
    is_direct = State()
