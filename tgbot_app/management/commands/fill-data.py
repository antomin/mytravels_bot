import requests
from django.core.management import BaseCommand
from django.db import IntegrityError

from tgbot_app.models import Country, City, Airport, Airline


class Command(BaseCommand):
    def handle(self, *args, **options):
        url_countries = 'https://api.travelpayouts.com/aviasales_resources/v3/countries.json?locale=ru'
        url_cities = 'https://api.travelpayouts.com/aviasales_resources/v3/cities.json?locale=ru'
        url_airports = 'https://api.travelpayouts.com/aviasales_resources/v3/airports.json?locale=ru'
        url_airlines = 'https://api.travelpayouts.com/aviasales_resources/v3/airlines.json?locale=ru'

        countries = self.get_request(url_countries)
        countries_len = len(countries)
        cnt = 1

        for country in countries:
            try:
                Country.objects.create(code=country['code'], title=country['name'])
                print(f'{cnt} страна из {countries_len} добавлена')
                cnt += 1
            except IntegrityError:
                pass

        cities = self.get_request(url_cities)
        cities_len = len(cities)
        cnt = 1

        for city in cities:
            try:
                country = Country.objects.get(code=city['country_code'])
                City.objects.create(code=city['code'], title=city['name'], country=country)
                print(f'{cnt} город из {cities_len} добавлен')
                cnt += 1
            except IntegrityError:
                pass

        airports = self.get_request(url_airports)
        airports_len = len(airports)
        cnt = 1

        for airport in airports:
            try:
                Airport.objects.create(code=airport['code'], title=airport['name'])
                print(f'{cnt} аэропорт из {airports_len} добавлен')
                cnt += 1
            except IntegrityError:
                pass

        airlines = self.get_request(url_airlines)
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

        print('DONE!')

    @staticmethod
    def get_request(url):
        headers = {
            'Accept-Encoding': 'gzip, deflate, br'
        }
        response = requests.get(url=url, headers=headers)
        return response.json()

