from asgiref.sync import sync_to_async
from django.core.paginator import Paginator
from django.db.models import QuerySet

from core import settings
from tgbot_app.models import (AviaCity, AviaCountry, ExcursionCity,
                              ExcursionCountry)


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
