from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from django.conf import settings

excursion_cd = CallbackData('excursion', 'action', 'value', 'page')


async def gen_excursion_countries_kb(countries, cur_page=None, has_prev=None, has_next=None):
    markup = InlineKeyboardMarkup(row_width=2)

    async for country in countries:
        markup.insert(InlineKeyboardButton(
            text=country.title, callback_data=excursion_cd.new(action='cities', value=country.id, page='1')))

    if has_prev:
        markup.add(InlineKeyboardButton(
            text='<<<', callback_data=excursion_cd.new(action='countries', value='0', page=cur_page - 1)))

    if has_next:
        markup.insert(InlineKeyboardButton(
            text='>>>', callback_data=excursion_cd.new(action='countries', value='0', page=cur_page + 1)))

    return markup


async def gen_excursion_cities_kb(cities, country_id, cur_page=None, has_prev=None, has_next=None):
    markup = InlineKeyboardMarkup(row_width=2)

    async for city in cities:
        markup.insert(InlineKeyboardButton(
            text=city.title, callback_data=excursion_cd.new(action='categories', value=city.id, page='1')))

    if has_prev:
        markup.add(InlineKeyboardButton(
            text='<<<', callback_data=excursion_cd.new(action='cities', value=country_id, page=cur_page - 1)))

    if has_next:
        markup.insert(InlineKeyboardButton(
            text='>>>', callback_data=excursion_cd.new(action='cities', value=country_id, page=cur_page + 1)))

    return markup


async def get_excursion_categories_kb(categories):
    markup = InlineKeyboardMarkup(row_width=2)

    for cat_id, cat in categories.items():
        markup.insert(
            InlineKeyboardButton(text=f'{cat["title"]}({cat["cnt"]})',
                                 callback_data=excursion_cd.new(action='product_list', value=cat_id, page='1'))
        )

    return markup


async def gen_products_kb(products, category_id=None, city_id=None, cur_page=None, has_prev=None, has_next=None):
    markup = InlineKeyboardMarkup(row_width=2)

    for prod in products:
        markup.add(InlineKeyboardButton(
            text=prod['name'], callback_data=excursion_cd.new(action='detail', value=str(prod['id']), page='0')))

    if has_prev:
        markup.add(InlineKeyboardButton(
            text='<<<', callback_data=excursion_cd.new(action='product_list', value=category_id, page=cur_page - 1)))

    if has_next:
        if not has_prev:
            markup.add(InlineKeyboardButton(
                text='>>>',
                callback_data=excursion_cd.new(action='product_list', value=category_id, page=cur_page + 1)))
        else:
            markup.insert(InlineKeyboardButton(
                text='>>>',
                callback_data=excursion_cd.new(action='product_list', value=category_id, page=cur_page + 1)))

    markup.add(InlineKeyboardButton(text='Назад к категориям', callback_data=excursion_cd.new(action='categories',
                                                                                              value=city_id, page='1')))

    return markup


async def gen_detail_kb(url, category_id, page_num):
    markup = InlineKeyboardMarkup(row_width=1)

    markup.add(InlineKeyboardButton(text='Забронировать', url=url))
    markup.add(InlineKeyboardButton(
        text='Назад к экскурсиям',
        callback_data=excursion_cd.new(action='product_list', value=category_id, page=page_num)
    ))

    return markup
