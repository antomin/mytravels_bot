from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message

from tgbot_app.keyboards import currency_cd, gen_help_currency_kb
from tgbot_app.loader import dp, exchange
from tgbot_app.utils.decos import reset_state
from tgbot_app.utils.text_variables import CURRENCY_TEXT


@dp.message_handler(Command('currency'), state='*')
@reset_state
async def start_handler(message: Message, state: FSMContext):
    await state.set_state('currency')
    markup = await gen_help_currency_kb()
    await message.answer(text=CURRENCY_TEXT, reply_markup=markup)


@dp.message_handler(state='currency')
async def answer_currency(message: Message):
    data = [el.strip() for el in message.text.split()]

    if len(data) == 2 and not data[0].isdigit() and not data[1].isdigit():
        text = await exchange.get_latest(data[0].upper(), data[1].upper())
    elif len(data) == 3 and data[0].isdigit() and not data[1].isdigit() and not data[2].isdigit():
        text = await exchange.get_convert(data[0], data[1].upper(), data[2].upper())
    else:
        markup = await gen_help_currency_kb()
        await message.answer(text='Мы не поняли Ваш запрос.\n' + CURRENCY_TEXT, reply_markup=markup)
        return

    if text:
        await message.answer(text=text)
    else:
        markup = await gen_help_currency_kb()
        await message.answer(text='Мы не поняли Ваш запрос.\n' + CURRENCY_TEXT, reply_markup=markup)
        return


@dp.callback_query_handler(currency_cd.filter(action='help'), state='*')
async def help_currency(callback: CallbackQuery):
    text = await exchange.get_symbols()
    await callback.message.answer(text=text)
