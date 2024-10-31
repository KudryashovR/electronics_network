import logging

from django.core.exceptions import ValidationError
from django.db import models


logger = logging.getLogger(__name__)


class NetworkNode(models.Model):
    """
    Модель "Звено сети", представляющая одно из звеньев иерархической сети.

    Эта модель содержит информацию о звене сети, включая его название, уровень иерархии, поставщика, контактную
    информацию и другие данные.
    """

    LEVEL_CHOICES = (
        (0, 'Завод'),
        (1, 'Розничная сеть'),
        (2, 'Индивидуальный предприниматель'),
    )

    name = models.CharField(max_length=255, verbose_name='Название')
    level = models.IntegerField(choices=LEVEL_CHOICES, verbose_name='Уровень иерархии')
    supplier = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='clients',
                                 verbose_name='Поставщик')

    email = models.EmailField(verbose_name='email')
    country = models.CharField(max_length=100, verbose_name='Страна')
    city = models.CharField(max_length=100, verbose_name='Город')
    street = models.CharField(max_length=100, verbose_name='Улица')
    house_number = models.CharField(max_length=10, verbose_name='Номер дома')

    created_at = models.DateTimeField(auto_now=True, verbose_name='Время создания')

    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Задолжность')

    def __str__(self):
        """
        Метод для возвращения строки, представляющей объект.

        :return: Название узла сети.
        """

        return self.name

    def get_full_address(self):
        """
        Метод для формирования полного адреса узла сети.

        :param self: Объект узла сети.
        :return: Полный адрес узла сети.
        """

        return f"{self.country}, {self.city}, {self.street}, {self.house_number}"

    def clean(self):
        """
        Метод для проверки валидности данных перед сохранением.

        :param self: Объект узла сети.
        :raise ValidationError: Исключение, если данные некорректны.
        """

        if self.level == 2 and self.supplier and self.supplier.level == 0:
            raise ValidationError({"level": "Завод не может иметь поставщика уровня 2."})
        super().clean()

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
        except ValidationError as e: # pragma: no cover
            logger.error(f'Ошибка валидации: {e.message_dict}') # pragma: no cover
            return # pragma: no cover

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Звено сети'
        verbose_name_plural = 'Звенья сети'


class Product(models.Model):
    """
    Модель продукта.

    Эта модель описывает продукт, включая его название, модель, дату выпуска и информацию о поставщике.
    """

    name = models.CharField(max_length=255, verbose_name='Название')
    model = models.CharField(max_length=100, verbose_name='Модель')
    release_date = models.DateField(verbose_name='Дата выпуска')

    supplier = models.ForeignKey(NetworkNode, on_delete=models.CASCADE, related_name='products',
                                 verbose_name='Поставщик')

    def __str__(self):
        """
        Возвращает строковое представление объекта.

        :return: Название и модель продукта в формате "Название (Модель)".
        """

        return f"{self.name} ({self.model})"

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
