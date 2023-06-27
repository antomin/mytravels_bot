from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message

from tgbot_app.models import Profile


class CheckProfileMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: Message, cb_data: dict):
        await Profile.objects.aget_or_create(tgid=message.from_user.id, first_name=message.from_user.first_name,
                                             last_name=message.from_user.last_name, username=message.from_user.username)

