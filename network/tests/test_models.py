from django.core.exceptions import ValidationError
from django.test import TestCase

from network.models import NetworkNode


class NetworkNodeModelTestCase(TestCase):
    """
    Класс для тестирования модели NetworkNode.

    Этот класс включает методы для тестирования различных аспектов работы модели, таких как формирование полного
    адреса и проверка валидации данных.
    """

    def setUp(self):
        """
        Подготовка тестовых данных.

        Создает экземпляр модели NetworkNode с необходимыми данными.
        """

        self.network_node = NetworkNode.objects.create(
            name='test',
            level=0,
            email='test@test.ts',
            country='test_country',
            city='test_city',
            street='test_street',
            house_number='21'
        )

    def test_get_full_address(self):
        """
        Тестирование метода get_full_address.

        Проверяет, что метод возвращает правильный формат полного адреса.
        """

        expected_str = 'test_country, test_city, test_street, 21'

        self.assertEqual(self.network_node.get_full_address(), expected_str)

    def test_clean_validation_error(self):
        """
        Тестирование метода clean на возникновение ошибки валидации.

        Проверяет, что при попытке создать узел сети с уровнем 2 и поставщиком уровня 0 возникает ошибка валидации.
        """

        network_node = NetworkNode(
            name='test',
            level=2,
            supplier=self.network_node,
            email='test@test.ts',
            country='test_country',
            city='test_city',
            street='test_street',
            house_number='21'
        )

        try:
            with self.assertLogs(level='ERROR') as logs:
                network_node.full_clean()
            self.assertIn('Ошибка валидации: {"level": ["Завод не может иметь поставщика уровня 2."]}',
                          logs.output[0])
        except ValidationError as e:
            self.assertDictEqual(e.message_dict, {"level": ["Завод не может иметь поставщика уровня 2."]})
        else:
            self.fail("ValidationError не был вызван")
