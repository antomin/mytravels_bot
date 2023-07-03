from aiogram import Dispatcher
from aiogram.utils import executor
from django.core.management.base import BaseCommand

from tgbot_app.handlers import dp
from tgbot_app.loader import scheduler
from tgbot_app.middlewares import (CheckProfileMiddleware,
                                   CheckSubscriptionMiddleware)
from tgbot_app.shedulers import check_flights, adv_mailing
from tgbot_app.utils import set_default_commands


async def register_middlewares(_dp: Dispatcher):
    _dp.setup_middleware(CheckProfileMiddleware())
    _dp.setup_middleware(CheckSubscriptionMiddleware())


async def add_scheduler_jobs():
    scheduler.add_job(check_flights, trigger='interval', minutes=10)
    scheduler.add_job(adv_mailing, trigger='interval', minutes=1)
    scheduler.start()


async def on_startup(_dp: Dispatcher):
    await set_default_commands(_dp)
    await register_middlewares(_dp)
    await add_scheduler_jobs()


class Command(BaseCommand):
    def handle(self, *args, **options):
        executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)
