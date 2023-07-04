from django.conf import settings
from django.shortcuts import redirect

from .models import Order
from tgbot_app.loader import robokassa


def success_payment(request):
    params = request.GET
    amount = params['OutSum']
    order_id = params['InvId']
    signature = params['SignatureValue']

    if robokassa.check_signature_result(order_id=order_id, amount=amount, received_signature=signature):
        order = Order.objects.get(id=int(order_id))
        order.user.subscribe()
        order.is_paid = True
        order.save()

    return redirect(f'https://t.me/{settings.TG_NAME}')


def result_payment(request):
    pass
