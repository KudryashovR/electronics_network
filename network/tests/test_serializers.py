from django.test import TestCase
from rest_framework.exceptions import ValidationError

from network.models import NetworkNode
from network.serializers import NetworkNodeSerializer


class NetworkNodeSerializerTests(TestCase):
    def setUp(self):
        self.supplier_level_0 = NetworkNode.objects.create(
            name='test_0',
            level=0,
            email='test@test.ts',
            country='test_country',
            city='test_city',
            street='test_street',
            house_number='21'
        )
        self.supplier_level_1 = NetworkNode.objects.create(
            name='test_1',
            level=1,
            email='test@test.ts',
            country='test_country',
            city='test_city',
            street='test_street',
            house_number='21'
        )

    def test_validate_level_with_supplier_level_0(self):
        data = {
            'name': 'test_1',
            'level': 2,
            'supplier': self.supplier_level_0.pk,
            'email': 'test@test.ts',
            'country': 'test_country',
            'city': 'test_city',
            'street': 'test_street',
            'house_number': '21'
        }
        serializer = NetworkNodeSerializer(data=data)

        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertIn('level', context.exception.detail)
        self.assertEqual(
            context.exception.detail['level'][0],
            'Завод не может иметь поставщика уровня 2.'
        )

    def test_validate_level_with_supplier_level_1(self):
        data = {
            'name': 'test_1',
            'level': 2,
            'supplier': self.supplier_level_1.pk,
            'email': 'test@test.ts',
            'country': 'test_country',
            'city': 'test_city',
            'street': 'test_street',
            'house_number': '21'
        }
        serializer = NetworkNodeSerializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            self.fail('ValidationError было вызвано при допустимых данных!')

    def test_validate_level_with_not_level_2(self):
        data = {
            'name': 'test_1',
            'level': 1,
            'supplier': self.supplier_level_0.pk,
            'email': 'test@test.ts',
            'country': 'test_country',
            'city': 'test_city',
            'street': 'test_street',
            'house_number': '21'
        }
        serializer = NetworkNodeSerializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            self.fail('ValidationError было вызвано при некорректных данных!')
