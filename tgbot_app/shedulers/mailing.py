import asyncio

from aiogram.types import InputFile, InputMediaPhoto
from django.conf import settings

from tgbot_app.keyboards import gen_adv_kb
from tgbot_app.loader import bot, semaphore_mailing
from tgbot_app.utils.common import notify_admins
from tgbot_app.utils.db_api import get_adv, get_all_objects, get_users_id
from tgbot_app.utils.decos import adv_sending_control


@adv_sending_control
async def _send_text_adv(user_id, text, markup):
    async with semaphore_mailing:
        await bot.send_message(chat_id=user_id, text=text, reply_markup=markup, disable_web_page_preview=True)
        return 1


@adv_sending_control
async def _send_photo_adv(user_id, text, photo_path, markup):
    photo = InputFile(photo_path)
    media_type = photo_path.split('.')[-1]

    async with semaphore_mailing:
        if media_type in ('mp4', 'gif'):
            await bot.send_animation(chat_id=user_id, animation=photo, caption=text, reply_markup=markup)
        else:
            await bot.send_photo(chat_id=user_id, photo=photo, caption=text, reply_markup=markup)

        return 1


@adv_sending_control
async def _send_mediagroup_adv(user_id, text, photos, markup):
    media = [InputMediaPhoto(InputFile(f'{settings.MEDIA_ROOT}/{photo.url}')) async for photo in photos]

    async with semaphore_mailing:
        await bot.send_media_group(chat_id=user_id, media=media)
        await bot.send_message(chat_id=user_id, text=text, reply_markup=markup, disable_web_page_preview=True)

        return 1


async def _adv_sending_process(adv, users):
    users_cnt = len(users)

    await notify_admins(f'Рассылка {adv.title} стартовала для {users_cnt} пользователей.')

    text = adv.text
    buttons = await get_all_objects(adv.buttons)
    photos = await get_all_objects(adv.photos)
    markup = await gen_adv_kb(buttons) if await buttons.acount() else None
    tasks = []

    if await photos.acount() == 0:
        for user_id in users:
            tasks.append(asyncio.create_task(_send_text_adv(user_id, text, markup)))

    elif await photos.acount() == 1:
        photo = await photos.afirst()
        photo_path = photo.url.path
        for user_id in users:
            tasks.append(asyncio.create_task(_send_photo_adv(user_id, text, photo_path, markup)))

    else:
        for user_id in users:
            tasks.append(asyncio.create_task(_send_mediagroup_adv(user_id, text, photos, markup)))

    result = await asyncio.gather(*tasks)

    await notify_admins(
        f'Рассылка {adv.title} была удачно доставлено {len([i for i in result if i == 1])} раз из {users_cnt}'
    )


async def adv_mailing():
    adverts = await get_adv()

    if not adverts['paid'] + adverts['unpaid'] + adverts['all']:
        return

    subscribed_users = await get_users_id(is_subscriber=True)
    unsubscribed_users = await get_users_id(is_subscriber=False)
    all_users = subscribed_users + unsubscribed_users

    if adverts['paid']:
        for adv in adverts['paid']:
            await _adv_sending_process(adv, subscribed_users)

    if adverts['unpaid']:
        for adv in adverts['unpaid']:
            await _adv_sending_process(adv, unsubscribed_users)

    if adverts['all']:
        for adv in adverts['all']:
            await _adv_sending_process(adv, all_users)
