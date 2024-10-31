from datetime import date, timedelta
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase

from network.models import NetworkNode, Product


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

    def test_product_creation(self):
        self.assertEqual(NetworkNode.objects.count(), 0)

        self.assertEqual(Product.objects.count(), 0)

        call_command('populate_network_nodes')
        call_command('populate_products')

        self.assertEqual(Product.objects.count(), 100)

        products = Product.objects.all()
        for product in products:
            self.assertIsNotNone(product.name)
            self.assertIsNotNone(product.model)
            self.assertIsNotNone(product.release_date)
            self.assertIsNotNone(product.supplier)

        today = date.today()
        five_years_ago = date.today() - timedelta(days=365 * 5)
        for product in products:
            self.assertLessEqual(product.release_date, today)
            self.assertGreaterEqual(product.release_date, five_years_ago)

    @patch('network.models.NetworkNode.objects.all')
    def test_no_network_nodes_message_and_return(self, mock_objects_all):
        mock_objects_all.return_value = []

        with self.assertLogs(level='ERROR') as logs:
            call_command('populate_products')

        self.assertIn("Звенья сети недоступны. Пожалуйста, сначала заполните их.", logs.output[0])

        self.assertEqual(Product.objects.count(), 0)
