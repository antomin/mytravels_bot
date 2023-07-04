from datetime import datetime

from asgiref.sync import sync_to_async
from django.core.paginator import Paginator
from django.db.models import QuerySet

from adv_app.models import Adv
from core import settings
from payments_app.models import Order
from tgbot_app.models import (AviaCity, AviaCountry, ExcursionCity,
                              ExcursionCountry, FlightSubscription, Profile)

from django.utils import timezone


@sync_to_async
def get_all_objects(obj):
    return obj.all()


@sync_to_async
def deactivate_user(user_id):
    try:
        user = Profile.objects.get(tgid=user_id)
        user.is_active = False
        user.save()
    except:
        pass


@sync_to_async
def get_avia_countries(search=None):
    if not search:
        return AviaCountry.objects.all()
    return AviaCountry.objects.filter(title__iregex=search.lower())


@sync_to_async
def get_avia_cities(country_code: str, search=None):
    if not search:
        return AviaCity.objects.filter(country__code=country_code)
    return AviaCity.objects.filter(country__code=country_code, title__iregex=search.lower())


@sync_to_async
def get_excursion_countries(search=None):
    if not search:
        return ExcursionCountry.objects.all()
    return ExcursionCountry.objects.filter(title__iregex=search.lower())


@sync_to_async
def get_excursion_cities(country_id: str, search=None):
    if not search:
        return ExcursionCity.objects.filter(country_id=country_id)
    return ExcursionCity.objects.filter(country_id=country_id, title__iregex=search.lower())


@sync_to_async
def gen_paginator(queryset: QuerySet, page_num: int, items_for_page=settings.ITEMS_FOR_PAGE) -> tuple:
    paginator = Paginator(queryset, items_for_page)
    page = paginator.page(page_num)

    return page.object_list, page.has_previous(), page.has_next()


@sync_to_async
def create_flight_subscription(user_id, flight, is_direct):
    new_sub = FlightSubscription(
        user=Profile.objects.get(tgid=user_id),
        depart_city=AviaCity.objects.get(code=flight['origin']),
        arrival_city=AviaCity.objects.get(code=flight['destination']),
        depart_date=datetime.fromisoformat(flight['departure_at']).date(),
        return_date=datetime.fromisoformat(flight['return_at']).date(),
        is_direct=True if is_direct == 'true' else False,
        last_price=flight['price']
    )
    new_sub.save()

    return new_sub.id


@sync_to_async
def del_flight_subscribe(sub_id):
    try:
        subscribe = FlightSubscription.objects.get(id=sub_id)
        subscribe.delete()
    except FlightSubscription.DoesNotExist:
        pass


@sync_to_async
def get_subscribes():
    return FlightSubscription.objects.all()


@sync_to_async
def get_subscribe_data(subscribe: FlightSubscription):
    return {
        'user_id': subscribe.user.tgid,
        'depart_code': subscribe.depart_city.code,
        'arrival_code': subscribe.arrival_city.code,
        'date_depart': datetime.strftime(subscribe.depart_date, '%Y-%m-%d'),
        'date_return': datetime.strftime(subscribe.return_date, '%Y-%m-%d') if subscribe.return_date else '',
        'is_direct': 'true' if subscribe.is_direct else 'false',
        'last_price': subscribe.last_price
    }


@sync_to_async
def get_adv():
    adverts = Adv.objects.filter(enabled=True)
    list_paid, list_unpaid, list_all = [], [], []
    for adv in adverts:
        if adv.time_exec <= timezone.now():
            adv.enabled = False
            adv.save()
            if adv.target == 'paid':
                list_paid.append(adv)
            elif adv.target == 'unpaid':
                list_unpaid.append(adv)
            else:
                list_all.append(adv)
    return {'paid': list_paid, 'unpaid': list_unpaid, 'all': list_all}


@sync_to_async
def get_users_id(is_subscriber=None):
    if is_subscriber is None:
        return [user.tgid for user in Profile.objects.filter(is_active=True)]
    return [user.tgid for user in Profile.objects.filter(is_active=True, is_subscriber=is_subscriber)]


@sync_to_async
def get_admins():
    return Profile.objects.filter(is_active=True, is_admin=True)


@sync_to_async
def gen_order(user_id, amount, prev_order=False):
    user = Profile.objects.get(tgid=user_id)
    order = Order.objects.create(user=user, amount=amount)
    if prev_order:
        prev_order = Order.objects.filter(user=user, is_paid=True).last()
        order.prev_order = prev_order
        order.save()
        return order.id, prev_order.id

    return order.id
