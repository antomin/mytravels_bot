from tgbot_app.keyboards import gen_flight_kb
from tgbot_app.models import FlightSubscription
from tgbot_app.utils.common import gen_avia_result_text
from tgbot_app.utils.db_api import get_subscribes, get_subscribe_data
from datetime import datetime
from tgbot_app.loader import bot, aviasales
import asyncio


async def notify_user(user_id, data, sub_id):
    text = await gen_avia_result_text(data)
    partner_url = await aviasales.gen_link(data['link'])
    markup = await gen_flight_kb(partner_url, is_sub=True, sub_id=sub_id)

    await bot.send_message(chat_id=user_id, text=text, reply_markup=markup)


async def make_request(subscribe: FlightSubscription):
    data = await get_subscribe_data(subscribe)
    result = await aviasales.search_flights(
        depart_code=data['depart_code'],
        arrival_code=data['arrival_code'],
        date_depart=data['date_depart'],
        date_return=data['date_return'],
        is_direct=data['is_direct'],
        one_result=True
    )

    if result[0]['price'] < data['last_price']:
        subscribe.last_price = result[0]['price']
        await subscribe.asave()
        await notify_user(user_id=subscribe.user.tgid, data=result[0], sub_id=subscribe.id)


async def check_flights():
    subscribes = await get_subscribes()
    tasks = []
    async for sub in subscribes:
        if sub.depart_date < datetime.now().date():
            await sub.adelete()
            await sub.asave()
            print('sub deleted')
        else:
            tasks.append(asyncio.create_task(make_request(sub)))

    await asyncio.gather(*tasks)
