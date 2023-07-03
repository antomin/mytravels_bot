from aiogram.types import Update

from tgbot_app.loader import dp


@dp.errors_handler()
async def error_handler(update: Update, exception: Exception):
    print(exception)
    try:
        await update.callback_query.message.answer(text='❌ Что-то пошло не так, попробуйте перезагрузить бота с '
                                                        'помощью команды /start и попробовать ещё раз.')
    except:
        await update.message.answer(text='❌ Что-то пошло не так, попробуйте перезагрузить бота с помощью '
                                         'команды /start и попробовать ещё раз.')
