from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from tgbot_app.loader import dp
from tgbot_app.utils.decos import reset_state
from tgbot_app.utils.text_variables import START_TEXT


@dp.message_handler(Command('start'), state='*')
@reset_state
async def start_handler(message: Message, state: FSMContext):
    await message.answer(text=START_TEXT)
