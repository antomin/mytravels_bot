from aiogram import Dispatcher
from aiogram.types import BotCommand


async def set_default_commands(dp: Dispatcher):
    await dp.bot.delete_my_commands()
    await dp.bot.set_my_commands([
        BotCommand('start', 'Перезапуск бота'),
        BotCommand('avia', 'Поиск авиабилетов'),
        BotCommand('currency', 'Курсы валют'),
        BotCommand('excursions', 'Экскурсии'),
        BotCommand('hotels', 'Поиск отелей'),
    ])
