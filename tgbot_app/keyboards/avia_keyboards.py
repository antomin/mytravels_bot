from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.callback_data import CallbackData

from django.conf import settings

avia_cd = CallbackData('avia', 'action', 'value', 'page')


async def gen_countries_kb(countries, target, cur_page, has_prev=None, has_next=None):
    markup = InlineKeyboardMarkup(row_width=2)

    async for country in countries:
        markup.insert(InlineKeyboardButton(
            text=country.title, callback_data=avia_cd.new(action='cities_page', value=country.code, page='1')))

    if has_prev:
        markup.add(InlineKeyboardButton(
            text='<<<', callback_data=avia_cd.new(action='countries_page' if target == 'depart' else 'set_city_depart',
                                                  value='0', page=cur_page - 1)))

    if has_next:
        markup.insert(InlineKeyboardButton(
            text='>>>', callback_data=avia_cd.new(action='countries_page' if target == 'depart' else 'set_city_depart',
                                                  value='0', page=cur_page + 1)))

    return markup


async def gen_cities_kb(cities, country_code, cur_page, target, has_prev=None, has_next=None):
    markup = InlineKeyboardMarkup(row_width=2)

    async for city in cities:
        markup.insert(InlineKeyboardButton(
            text=city.title, callback_data=avia_cd.new(action=f'set_city_{target}', value=city.code, page='1')))

    if has_prev:
        markup.add(InlineKeyboardButton(
            text='<<<', callback_data=avia_cd.new(action='cities_page', value=country_code, page=cur_page - 1)))

    if has_next:
        markup.insert(InlineKeyboardButton(
            text='>>>', callback_data=avia_cd.new(action='cities_page', value=country_code, page=cur_page + 1)))

    return markup


async def gen_num_people_kb():
    markup = InlineKeyboardMarkup(row_width=5)

    for i in range(1, 11):
        markup.insert(InlineKeyboardButton(text=str(i), callback_data=avia_cd.new(action='set_num_people', value=str(i),
                                                                                  page='0')))

    return markup


async def gen_direct_kb():
    markup = InlineKeyboardMarkup(row_width=2)

    markup.add(
        InlineKeyboardButton(text='Нет', callback_data=avia_cd.new(action='set_direct', value='true', page='0')),
        InlineKeyboardButton(text='Да', callback_data=avia_cd.new(action='set_direct', value='false', page='0'))
    )

    return markup


async def gen_flight_kb(url):
    return InlineKeyboardMarkup().add(InlineKeyboardButton(text='Забронировать',
                                                           url=f'{settings.AVIASALES_PARTNER_URL}{url}'))
