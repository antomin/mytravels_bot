from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from django.conf import settings

from tgbot_app.loader import robokassa
from tgbot_app.utils.db_api import gen_order


async def gen_payment_kb(user_id, amount=settings.SUBSCRIPTION_PRICE):
    markup = InlineKeyboardMarkup(row_width=1)

    order_id = await gen_order(user_id=user_id, amount=amount)
    payment_url = robokassa.gen_payment_link(user_id=user_id, order_id=order_id)

    markup.add(InlineKeyboardButton(text='Поддержать', url=payment_url))

    return markup
