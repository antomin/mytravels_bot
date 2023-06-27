from aiogram import Dispatcher
from aiogram.utils import executor
from django.core.management.base import BaseCommand
from tgbot_app.utils import set_default_commands
from tgbot_app.handlers import dp
from tgbot_app.middlewares import CheckProfileMiddleware, CheckSubscriptionMiddleware


async def register_middlewares(_dp: Dispatcher):
    _dp.setup_middleware(CheckProfileMiddleware())
    _dp.setup_middleware(CheckSubscriptionMiddleware())


async def on_startup(_dp: Dispatcher):
    await set_default_commands(_dp)
    await register_middlewares(_dp)


class Command(BaseCommand):
    def handle(self, *args, **options):
        executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)
