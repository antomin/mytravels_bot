from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from django.conf import settings

from tgbot_app.utils.services_api import Aviasales, Sputnik, Exchangerate

storage = MemoryStorage()
bot = Bot(token=settings.TG_TOKEN, parse_mode='html')
dp = Dispatcher(bot=bot, storage=storage)
scheduler = AsyncIOScheduler()

aviasales = Aviasales(token=settings.AVIASALES_API_TOKEN)
sputnik = Sputnik(token=settings.SPUTNIK_API_TOKEN, username=settings.SPUTNIK_USERNAME)
exchange = Exchangerate()
