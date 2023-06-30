from asgiref.sync import sync_to_async
from django.core.paginator import Paginator
from django.db.models import QuerySet

from datetime import datetime

from adv_app.models import Adv
from core import settings
from tgbot_app.models import (AviaCity, AviaCountry, ExcursionCity,
                              ExcursionCountry, FlightSubscription, Profile)


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
    return Adv.objects.filter()
