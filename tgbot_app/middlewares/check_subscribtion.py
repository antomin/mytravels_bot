from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message

from django.conf import settings

from tgbot_app.loader import bot
from tgbot_app.utils.text_variables import CHECK_SUBSCRIPTION_TEXT


class CheckSubscriptionMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: Message, cb_data: dict):
        status = await bot.get_chat_member(chat_id=settings.CHANNEL_ID, user_id=message.from_user.id)

        if status['status'] in ('left', 'banned'):
            await message.answer(
                text=CHECK_SUBSCRIPTION_TEXT.format(link=settings.CHANNEL_LINK, name=settings.CHANNEL_NAME)
            )

            raise CancelHandler()
