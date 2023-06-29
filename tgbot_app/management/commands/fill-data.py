import time

import requests
from django.conf import settings
from django.core.management import BaseCommand
from django.db import IntegrityError

from tgbot_app.models import (Airline, Airport, AviaCity, AviaCountry,
                              ExcursionCity, ExcursionCountry)


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.fill_avia_countries()
        self.fill_avia_cities()
        self.fill_airlines()
        self.fill_airports()

        self.fill_excursions_countries()
        self.fill_excursions_cities()

    def fill_avia_countries(self):
        url = 'https://api.travelpayouts.com/aviasales_resources/v3/countries.json?locale=ru'
        countries = self.get_aviasales_request(url)
        countries_len = len(countries)
        cnt = 1

        for country in countries:
            try:
                AviaCountry.objects.create(code=country['code'], title=country['name'])
                print(f'{cnt} страна из {countries_len} добавлена')
                cnt += 1
            except IntegrityError:
                pass

    def fill_avia_cities(self):
        url = 'https://api.travelpayouts.com/aviasales_resources/v3/cities.json?locale=ru'
        cities = self.get_aviasales_request(url)
        cities_len = len(cities)
        cnt = 1

        for city in cities:
            try:
                country = AviaCountry.objects.get(code=city['country_code'])
                AviaCity.objects.create(code=city['code'], title=city['name'], country=country)
                print(f'{cnt} город из {cities_len} добавлен')
                cnt += 1
            except IntegrityError:
                pass

    def fill_airports(self):
        url = 'https://api.travelpayouts.com/aviasales_resources/v3/airports.json?locale=ru'
        airports = self.get_aviasales_request(url)
        airports_len = len(airports)
        cnt = 1

        for airport in airports:
            try:
                Airport.objects.create(code=airport['code'], title=airport['name'])
                print(f'{cnt} аэропорт из {airports_len} добавлен')
                cnt += 1
            except IntegrityError:
                pass

    def fill_airlines(self):
        url = 'https://api.travelpayouts.com/aviasales_resources/v3/airlines.json?locale=ru'
        airlines = self.get_aviasales_request(url)
        airlines_len = len(airlines)
        cnt = 1

        for airline in airlines:
            try:
                title = airline['name'] if airline['name'] else airline['name_translations']['en']
                Airline.objects.create(code=airline['code'], title=title)
                print(f'{cnt} авиакомпания из {airlines_len} добавлена')
                cnt += 1
            except IntegrityError:
                pass

    def fill_excursions_countries(self):
        url = 'https://api.sputnik8.com/v1/countries'
        page = 1
        all_countries = []
        cnt = 1

        while True:
            countries = self.get_sputnik_request(url, page)
            if not countries:
                break
            all_countries += countries
            time.sleep(2)
            page += 1

        countries_len = len(all_countries)

        for country in all_countries:
            try:
                ExcursionCountry.objects.create(id=country['id'], title=country['name'])
                print(f'{cnt} страна из {countries_len} добавлена')
                cnt += 1
            except IntegrityError as error:
                print(error)
                pass

    def fill_excursions_cities(self):
        url = 'https://api.sputnik8.com/v1/cities'
        page = 1
        all_cities = []
        cnt = 1

        while True:
            cities = self.get_sputnik_request(url, page)
            if not cities:
                break
            all_cities += cities
            time.sleep(2)
            page += 1

        cities_len = len(all_cities)

        for city in all_cities:
            try:
                country = ExcursionCountry.objects.get(id=city['country_id'])
                ExcursionCity.objects.create(id=city['id'], title=city['name'], country=country)
                print(f'{cnt} город из {cities_len} добавлена')
                cnt += 1
            except IntegrityError as error:
                print(error)
                pass

    @staticmethod
    def get_aviasales_request(url):
        headers = {
            'Accept-Encoding': 'gzip, deflate, br'
        }
        response = requests.get(url=url, headers=headers)
        return response.json()

    @staticmethod
    def get_sputnik_request(url, page=None):
        params = {
            'api_key': settings.SPUTNIK_API,
            'username': settings.SPUTNIK_USERNAME,
            'limit': 20
        }
        if page:
            params['page'] = page

        response = requests.get(url, params=params)

        return response.json()
