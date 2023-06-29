from django.core.management import BaseCommand

from tgbot_app.models import (Airline, Airport, AviaCity, AviaCountry,
                              ExcursionCity, ExcursionCountry)


class Command(BaseCommand):
    def handle(self, *args, **options):
        models = (
            AviaCountry,
            AviaCity,
            Airport,
            Airline,
            ExcursionCountry,
            ExcursionCity,
        )

        for model in models:
            self.del_items(model)

    @staticmethod
    def del_items(model):
        items = model.objects.all()
        for item in items:
            item.delete()
            item.save()

        print('DONE!!!')

