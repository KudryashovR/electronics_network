from django.core.management import call_command
from django.test import TestCase

from network.models import NetworkNode


class CommandTestCase(TestCase):

    def test_command_creates_network_nodes(self):
        self.assertEqual(NetworkNode.objects.count(), 0)

        call_command('populate_network_nodes')

        self.assertEqual(NetworkNode.objects.count(), 100)

        level_0_nodes = NetworkNode.objects.filter(level=0)
        level_1_nodes = NetworkNode.objects.filter(level=1)
        level_2_nodes = NetworkNode.objects.filter(level=2)

        self.assertEqual(level_0_nodes.count(), 10)
        self.assertEqual(level_1_nodes.count(), 30)
        self.assertEqual(level_2_nodes.count(), 60)

        for node in level_1_nodes:
            self.assertIsNotNone(node.supplier)
            self.assertEqual(node.supplier.level, 0)

        for node in level_2_nodes:
            self.assertIsNotNone(node.supplier)
            self.assertIn(node.supplier.level, [0, 1, 2])

        for node in NetworkNode.objects.all():
            self.assertIsNotNone(node.name)
            self.assertIsNotNone(node.email)
            self.assertIsNotNone(node.country)
            self.assertIsNotNone(node.city)
            self.assertIsNotNone(node.street)
            self.assertIsNotNone(node.house_number)