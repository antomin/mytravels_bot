from django.core.management import BaseCommand

from tgbot_app.models import Country, City, Airport, Airline


class Command(BaseCommand):
    def handle(self, *args, **options):
        for model in (Country, City, Airport, Airline):
            self.del_items(model)

    @staticmethod
    def del_items(model):
        items = model.objects.all()
        for item in items:
            item.delete()
            item.save()

        print('DONE!!!')

