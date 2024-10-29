from django.contrib import admin

from network.models import NetworkNode, Product


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    """
    Класс администратора для модели NetworkNode.

    В этом классе настраиваются отображение полей в списке, поисковые поля, фильтры списка, а также дополнительные
    методы и действия администраторов.
    """

    list_display = ['name', 'level', 'get_full_address', 'debt', 'created_at']
    search_fields = ['name', 'city']
    list_filter = ['city']

    get_full_address = lambda self, obj: obj.get_full_address()
    get_full_address.short_description = 'Полный адрес'

    actions = ['clear_debt']

    @admin.action(description='Очистить задолжность')
    def clear_debt(self, request, queryset):
        """
        Очищает задолженность у выбранных объектов.

        :param request: Запрос от пользователя.
        :param queryset: Набор объектов, к которым применяется действие.
        """

        queryset.update(debt=0.00)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Класс администратора для модели Product.

    Этот класс определяет настройки отображения и управления продуктами в административной панели Django.
    """

    list_display = ['name', 'model', 'release_date', 'supplier']
