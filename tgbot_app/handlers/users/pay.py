from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from tgbot_app.keyboards import gen_payment_kb
from tgbot_app.loader import dp
from tgbot_app.utils.decos import reset_state


@dp.message_handler(Command('pay'))
@reset_state
async def payment_start(message: Message, state: FSMContext):
    text = 'Нажимая кнопку ниже я даю согласие на регулярные списания, на обработку персональных данных и принимаю ' \
           'условия публичной оферты.'
    markup = await gen_payment_kb(user_id=message.from_user.id)

    await message.answer(text=text, reply_markup=markup)
