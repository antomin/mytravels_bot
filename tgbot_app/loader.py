from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from django.conf import settings

from tgbot_app.utils.aviasales_api import Aviasales

storage = MemoryStorage()
bot = Bot(token=settings.TG_TOKEN, parse_mode='html')
dp = Dispatcher(bot=bot, storage=storage)
scheduler = AsyncIOScheduler()

aviasales = Aviasales(token=settings.AVIASALES_TOKEN)
