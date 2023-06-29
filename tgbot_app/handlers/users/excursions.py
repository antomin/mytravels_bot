from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, MediaGroup, Message
from django.conf import settings

from tgbot_app.keyboards import (excursion_cd, gen_detail_kb,
                                 gen_excursion_cities_kb,
                                 gen_excursion_countries_kb, gen_products_kb,
                                 get_excursion_categories_kb)
from tgbot_app.loader import dp, sputnik
from tgbot_app.states import ExcursionState
from tgbot_app.utils.common import gen_excursion_result_text
from tgbot_app.utils.db_api import (gen_paginator, get_excursion_cities,
                                    get_excursion_countries)
from tgbot_app.utils.decos import reset_state


@dp.callback_query_handler(excursion_cd.filter(action='countries'), state='*')
@dp.message_handler(Command('excursions'), state='*')
@reset_state
async def excursion_countries(message: Message | CallbackQuery, state: FSMContext):
    if isinstance(message, CallbackQuery):
        await message.answer()
        page_num = int(message.data.split(':')[-1])
        message = message.message
    else:
        page_num = 1

    countries = await get_excursion_countries()
    queryset, has_prev, has_next = await gen_paginator(countries, page_num)
    markup = await gen_excursion_countries_kb(countries=queryset, cur_page=page_num, has_prev=has_prev,
                                              has_next=has_next)

    await message.answer(text='Выберите страну из списка или напишите для быстрого поиска:',
                         reply_markup=markup)

    await ExcursionState.country.set()


@dp.callback_query_handler(excursion_cd.filter(action='cities'), state='*')
async def excursion_cities(callback: CallbackQuery, callback_data: dict, state: FSMContext):
    country_id = callback_data.get('value')
    page_num = int(callback_data.get('page'))
    cities = await get_excursion_cities(country_id=country_id)
    queryset, has_prev, has_next = await gen_paginator(cities, page_num)

    markup = await gen_excursion_cities_kb(cities=queryset, country_id=country_id, cur_page=page_num, has_prev=has_prev,
                                           has_next=has_next)

    await callback.message.answer(text=f'Выберите город из списка или напишите для быстрого поиска:',
                                  reply_markup=markup)
    await callback.answer()

    async with state.proxy() as data:
        data['country_id'] = country_id
    await ExcursionState.city.set()


@dp.message_handler(state=ExcursionState.country)
async def filter_country(message: Message, state: FSMContext):
    countries = await get_excursion_countries(search=message.text)

    if not await countries.acount():
        await message.answer('Не найдено подходящих стран.\nПопробуйте ещё раз или выберите из списка выше.')
        return

    markup = await gen_excursion_countries_kb(countries=countries)
    await message.answer(text='Выберите страну:', reply_markup=markup)

    await state.reset_state()


@dp.message_handler(state=ExcursionState.city)
async def filter_city(message: Message, state: FSMContext):
    async with state.proxy() as data:
        country_id = data['country_id']

    cities = await get_excursion_cities(country_id=country_id, search=message.text)

    if not await cities.acount():
        await message.answer('Не найдено подходящих стран.\nПопробуйте ещё раз или выберите из списка выше.')
        return

    markup = await gen_excursion_cities_kb(cities=cities, country_id=country_id)
    await message.answer(text=f'Выберите город:', reply_markup=markup)


@dp.callback_query_handler(excursion_cd.filter(action='categories'), state='*')
async def excursion_categories(callback: CallbackQuery, callback_data: dict, state: FSMContext):
    status = await callback.message.answer('Обновляем актуальную информацию ⏳\nЭто может занять до 1мин.')
    await callback.answer()

    city_id = callback_data.get('value')

    async with state.proxy() as data:
        categories = data.get('categories', None)
        data['city_id'] = city_id

        if categories is None:
            categories = await sputnik.get_categories(city_id=city_id)
            data['categories'] = categories

    if not categories:
        await status.edit_text('К сожалению в этом городе нет проверенных экскурсий')

    markup = await get_excursion_categories_kb(categories)
    await status.delete()
    await callback.message.answer(text='Выберите категорию:', reply_markup=markup)


@dp.callback_query_handler(excursion_cd.filter(action='product_list'), state='*')
async def excursion_product_list(callback: CallbackQuery, callback_data: dict, state: FSMContext):
    category_id = callback_data.get('value')
    page_num = int(callback_data.get('page'))
    async with state.proxy() as data:
        categories = data.get('categories')
        data['category_id'] = category_id
        data['page_num'] = page_num
        city_id = data['city_id']

    products = categories[category_id]['products']
    queryset, has_prev, has_next = await gen_paginator(products, page_num, settings.EXCURSIONS_FOR_PAGE)

    markup = await gen_products_kb(
        products=queryset, category_id=category_id, city_id=city_id, cur_page=page_num, has_prev=has_prev,
        has_next=has_next
    )

    await callback.message.answer(text='Выберите понравившуюся экскурсию чтобы увидеть детали:', reply_markup=markup)
    await callback.answer()


@dp.callback_query_handler(excursion_cd.filter(action='detail'), state='*')
async def excursion_detail(callback: CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    status = await callback.message.answer('Загружаем подробную информацию ⏳')
    product_id = int(callback_data.get('value'))

    async with state.proxy() as data:
        category_id = data['category_id']
        page_num = data['page_num']

    data = await sputnik.get_product_detail(product_id)

    text = await gen_excursion_result_text(data)
    media_group = MediaGroup()
    for photo in data['photos']:
        media_group.attach_photo(photo=photo['big'])
    markup = await gen_detail_kb(url=data['url'], category_id=category_id, page_num=page_num)

    await callback.message.answer_media_group(media=media_group)
    await callback.message.answer(text=text, reply_markup=markup)
    await status.delete()

