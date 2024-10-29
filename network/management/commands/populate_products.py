import random

from django.core.management import BaseCommand
from faker import Faker

from network.models import NetworkNode, Product


class Command(BaseCommand):
    help = "Заполнение 100 случайных значений в модель Product"

    def handle(self, *args, **kwargs):
        fake = Faker()
        nodes = list(NetworkNode.objects.all())

        if not nodes:
            print("Звенья сети недоступны. Пожалуйста, сначала заполните их.")
            return

        for _ in range(100):
            supplier = random.choice(nodes)
            product = Product(
                name=fake.word(),
                model=fake.lexify(text='Model-????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
                release_date=fake.date_between(start_date='-5y', end_date='today'),
                supplier=supplier
            )
            product.save()
