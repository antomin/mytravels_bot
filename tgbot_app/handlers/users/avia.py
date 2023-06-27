from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from tgbot_app.keyboards import avia_cd, gen_countries_kb, gen_cities_kb, gen_direct_kb, \
    gen_flight_kb
from tgbot_app.loader import dp, aviasales
from tgbot_app.states import AviaState
from tgbot_app.utils.common import date_validate, gen_avia_result_text
from tgbot_app.utils.db_api import get_countries, get_cities, gen_paginator


@dp.callback_query_handler(avia_cd.filter(action='countries_page'), state=AviaState)
@dp.message_handler(Command('avia'), state='*')
async def countries_list(message: Message | CallbackQuery, state: FSMContext):
    target = 'depart'

    await AviaState.depart.set()
    async with state.proxy() as data:
        data['target'] = target

    if isinstance(message, CallbackQuery):
        await message.answer()
        page_num = int(message.data.split(':')[-1])
        message = message.message
    else:
        page_num = 1

    countries = await get_countries()
    queryset, has_prev, has_next = await gen_paginator(countries, page_num)

    markup = await gen_countries_kb(countries=queryset, target=target, cur_page=page_num, has_next=has_next,
                                    has_prev=has_prev)
    await message.answer(text='Выберите страну отправления:', reply_markup=markup)


@dp.callback_query_handler(avia_cd.filter(action='cities_page'), state=AviaState)
async def cities_list(callback: CallbackQuery, callback_data: dict, state: FSMContext):
    country_code = callback_data.get('value')
    page_num = int(callback_data.get('page'))

    async with state.proxy() as data:
        target = data['target']

    cities = await get_cities(country_code)
    queryset, has_prev, has_next = await gen_paginator(cities, page_num)

    markup = await gen_cities_kb(cities=queryset, country_code=country_code, cur_page=page_num, has_next=has_next,
                                 has_prev=has_prev, target=target)

    await callback.message.answer(text=f'Выберите город {"отправления" if target == "depart" else "прибытия"}:',
                                  reply_markup=markup)
    await callback.answer()


@dp.callback_query_handler(avia_cd.filter(action='set_city_depart'), state=AviaState)
async def set_departure(callback: CallbackQuery, callback_data: dict, state: FSMContext):
    depart_code = callback_data.get('value')
    page_num = int(callback_data.get('page'))
    target = 'arrival'

    if page_num == 1:
        async with state.proxy() as data:
            data['depart'] = depart_code
            data['target'] = target

    countries = await get_countries()
    queryset, has_prev, has_next = await gen_paginator(countries, page_num)

    markup = await gen_countries_kb(countries=queryset, target=target, cur_page=page_num, has_next=has_next,
                                    has_prev=has_prev)
    await callback.message.answer(text='Выберите страну прибытия:', reply_markup=markup)
    await callback.answer()
    await AviaState.arrival.set()


@dp.callback_query_handler(avia_cd.filter(action='set_city_arrival'), state=AviaState.arrival)
async def set_departure(callback: CallbackQuery, callback_data: dict, state: FSMContext):
    arrival_code = callback_data.get('value')
    async with state.proxy() as data:
        data['arrival'] = arrival_code
        del data['target']

    await callback.message.answer(text='Напишите дату отправления в формате ГГГГ-ММ-ДД:')
    await callback.answer()
    await AviaState.date_depart.set()


@dp.message_handler(state=AviaState.date_depart)
async def set_depart_date(message: Message, state: FSMContext):
    date = message.text
    if not await date_validate(date):
        await message.answer('Вы неверно ввели дату.\nНапишите дату в формате ГГГГ-ММ-ДД:')
        return

    async with state.proxy() as data:
        data['date_depart'] = date

    await message.answer(text='Напишите дату возвращения в формате ГГГГ-ММ-ДД\n'
                              'Если Вам нужен билет в одну сторону, отправьте "-":')
    await AviaState.date_return.set()


@dp.message_handler(state=AviaState.date_return)
async def set_depart_date(message: Message, state: FSMContext):
    date = message.text
    if date != '-' and not await date_validate(date):
        await message.answer('Вы неверно ввели дату.\nНапишите дату в формате ГГГГ-ММ-ДД:')
        return

    async with state.proxy() as data:
        data['date_return'] = None if date == '-' else date

    markup = await gen_direct_kb()
    await message.answer(text='Подыскать Вам рейсы с пересадками?', reply_markup=markup)
    await AviaState.is_direct.set()


@dp.callback_query_handler(avia_cd.filter(action='set_direct'), state=AviaState.is_direct)
async def set_direct(callback: CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()

    status = await callback.message.answer(text='Мы подбираем дешевые авиабилеты ⏳')

    is_direct = callback_data.get('value')
    async with state.proxy() as data:
        depart_code = data['depart']
        arrival_code = data['arrival']
        date_depart = data['date_depart']
        date_return = data['date_return']

    data = await aviasales.search_flights(
        depart_code=depart_code,
        arrival_code=arrival_code,
        date_depart=date_depart,
        date_return=date_return,
        is_direct=is_direct
    )

    await status.delete()

    if not data:
        await callback.message.answer('К сожалению на выбранную дату нет рейсов')
        return

    for flight in data:
        text = await gen_avia_result_text(flight)
        markup = await gen_flight_kb(flight['link'])

        await callback.message.answer(text=text, reply_markup=markup)
