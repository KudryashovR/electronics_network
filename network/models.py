from django.db import models


class NetworkNode(models.Model):
    """
    Модель звена сети.

    Эта модель представляет собой узел сети, который может иметь различных поставщиков и клиентов.
    У каждого узла есть название, уровень иерархии, поставщики, контактные данные и информация о местоположении.
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
        Возвращает строковое представление объекта.

        :return: Название узла.
        """

        return self.name

    def get_full_address(self):
        """
        Формирует полный адрес узла.

        :return: Строка с полным адресом узла.
        """

        return f"{self.country}, {self.city}, {self.street}, {self.house_number}"

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
