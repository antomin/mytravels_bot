import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from django.conf import settings

from api import Aviasales, Exchangerate, Sputnik, Robokassa

storage = MemoryStorage()
bot = Bot(token=settings.TG_TOKEN, parse_mode='html')
dp = Dispatcher(bot=bot, storage=storage)
scheduler = AsyncIOScheduler()

semaphore_mailing = asyncio.Semaphore(20)

aviasales = Aviasales(token=settings.AVIASALES_API_TOKEN, marker=settings.AVIASALES_MARKER)
sputnik = Sputnik(token=settings.SPUTNIK_API_TOKEN, username=settings.SPUTNIK_USERNAME)
exchange = Exchangerate()
robokassa = Robokassa(login=settings.ROBOKASSA_LOGIN, pass_1=settings.ROBOKASSA_PASS_1,
                      pass_2=settings.ROBOKASSA_PASS_2)
