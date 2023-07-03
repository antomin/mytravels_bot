from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def gen_adv_kb(buttons):
    markup = InlineKeyboardMarkup(row_width=1)

    async for button in buttons:
        markup.add(InlineKeyboardButton(text=button.title, url=button.url))

    return markup
