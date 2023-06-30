from aiogram import Dispatcher
from aiogram.types import BotCommand


async def set_default_commands(dp: Dispatcher):
    await dp.bot.delete_my_commands()
    await dp.bot.set_my_commands([
        BotCommand('start', 'Перезапуск бота'),
        BotCommand('avia', 'Поиск авиабилетов'),
        BotCommand('avia_sub', 'Подписка на билеты'),
        BotCommand('excursions', 'Экскурсии'),
        BotCommand('currency', 'Курсы валют'),
    ])
