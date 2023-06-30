from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

currency_cd = CallbackData('currency', 'action')


async def gen_help_currency_kb():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(text='Доступные валюты', callback_data=currency_cd.new(action='help')))

