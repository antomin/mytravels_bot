from datetime import timedelta

from django.conf import settings

from tgbot_app.loader import bot, robokassa
from tgbot_app.models import Profile
from tgbot_app.utils.db_api import get_users_id, gen_order
from django.utils import timezone


async def _check_user(user_id):
    user = await Profile.objects.aget(tgid=user_id)
    if user.is_subscriber and user.end_subscription <= timezone.now():
        if user.pay_cnt < 4:
            user.end_subscription += timedelta(hours=24 if user.pay_cnt == 1 else 12)
            user.pay_cnt += 1
            await user.asave()

            order_id, prev_order_id = await gen_order(user_id=user_id, amount=settings.SUBSCRIPTION_PRICE,
                                                      prev_order=True)
            await robokassa.send_recurring_payment(user_id=user_id, order_id=order_id, prev_payment=prev_order_id)

        else:
            await user.unsubscribe()
            return 'unsubscribed'


async def check_users_subscription():
    users = await get_users_id()
    for user_id in users:
        result = await _check_user(user_id)
        if result == 'unsubscribed':
            await bot.send_message(
                chat_id=user_id,
                text='К сожалению мы не получили от вас оплату для продления подписки, по этому подписка была '
                     'аннулирована. Надеемся что вы вернетесь к нам.'
            )
