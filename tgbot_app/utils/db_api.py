from asgiref.sync import sync_to_async
from django.core.paginator import Paginator
from django.db.models import QuerySet

from core import settings
from tgbot_app.models import Country, City


@sync_to_async
def get_countries():
    return Country.objects.all()


@sync_to_async
def get_cities(country_code: str):
    return City.objects.filter(country__code=country_code)


@sync_to_async
def gen_paginator(queryset: QuerySet, page_num: int) -> tuple:
    paginator = Paginator(queryset, settings.ITEMS_FOR_PAGE)
    page = paginator.page(page_num)

    return page.object_list, page.has_previous(), page.has_next()
