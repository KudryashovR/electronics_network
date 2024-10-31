from django.contrib.admin import site
from django.test import TestCase, RequestFactory

from network.admin import NetworkNodeAdmin
from network.models import NetworkNode


class NetworkNodeAdminTests(TestCase):
    """
    Класс для тестирования администратора модели NetworkNode.

    Этот класс включает методы для тестирования функционала очистки задолженности.
    """

    def setUp(self):
        """
        Настройка тестовой среды.

        Создаются два экземпляра модели NetworkNode с различными значениями долга. Также создается запрос
        и инстанцируется администратор модели.
        """

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
        """
        Тестирование функции clear_debt администратора.

        Проверяет, что после вызова функции clear_debt долг выбранных экземпляров модели становится равным нулю.
        """

        queryset = NetworkNode.objects.filter(pk__in=[self.instance1.pk, self.instance2.pk])
        self.admin_instance.clear_debt(self.request, queryset)

        self.instance1.refresh_from_db()
        self.instance2.refresh_from_db()

        self.assertEqual(self.instance1.debt, 0.00)
        self.assertEqual(self.instance2.debt, 0.00)
