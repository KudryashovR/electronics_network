from django.contrib.admin import site
from django.test import TestCase, RequestFactory

from network.admin import NetworkNodeAdmin
from network.models import NetworkNode


class NetworkNodeAdminTests(TestCase):

    def setUp(self):
        self.instance1 = NetworkNode.objects.create(
            name='Node1',
            level=1,
            email='node1@example.com',
            country='Country1',
            city='City1',
            street='Street1',
            house_number='1',
            debt=100.00
        )
        self.instance2 = NetworkNode.objects.create(
            name='Node2',
            level=1,
            email='node2@example.com',
            country='Country2',
            city='City2',
            street='Street2',
            house_number='2',
            debt=200.00
        )
        self.request = RequestFactory().get('/admin/NetworkNode/')
        self.admin_instance = NetworkNodeAdmin(NetworkNode, site)

    def test_clear_debt(self):
        queryset = NetworkNode.objects.filter(pk__in=[self.instance1.pk, self.instance2.pk])
        self.admin_instance.clear_debt(self.request, queryset)

        self.instance1.refresh_from_db()
        self.instance2.refresh_from_db()

        self.assertEqual(self.instance1.debt, 0.00)
        self.assertEqual(self.instance2.debt, 0.00)