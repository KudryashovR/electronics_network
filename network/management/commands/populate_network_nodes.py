import random

from django.core.management import BaseCommand
from faker import Faker

from network.models import NetworkNode


class Command(BaseCommand):
    help = "Заполнение 100 случайных значений в модель NetworkNode"

    def handle(self, *args, **kwargs):
        fake = Faker()
        nodes = []

        for _ in range(10):
            node = NetworkNode(name=fake.company(), level=0, supplier=None, email=fake.company_email(),
                               country=fake.country(), city=fake.city(), street=fake.street_name(),
                               house_number=fake.building_number(), debt=0.00)
            node.save()
            nodes.append(node)

        for _ in range(30):
            supplier = random.choice([node for node in nodes if node.level == 0])
            node = NetworkNode(name=fake.company(), level=1, supplier=supplier, email=fake.company_email(),
                               country=fake.country(), city=fake.city(), street=fake.street_name(),
                               house_number=fake.building_number(), debt=round(random.uniform(0, 1000), 2))
            node.save()
            nodes.append(node)

        for _ in range(60):
            supplier = random.choice(nodes)
            node = NetworkNode(name=fake.company(), level=2, supplier=supplier, email=fake.company_email(),
                               country=fake.country(), city=fake.city(), street=fake.street_name(),
                               house_number=fake.building_number(), debt=round(random.uniform(0, 1000), 2))
            node.save()
            nodes.append(node)
