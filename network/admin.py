from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from network.models import NetworkNode, Product


def get_full_address(obj):
    return obj.get_full_address()


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    """
    Класс администратора для модели NetworkNode.

    Этот класс определяет настройки отображения и управления узлами сети в административной панели Django.
    """

    list_display = ['name', 'level', 'get_supplier_link', 'get_full_address', 'debt', 'created_at']
    search_fields = ['name', 'city']
    list_filter = ['city']

    def get_full_address(self, obj):
        """
        Получение полного адреса узла сети.

        :param obj: Объект узла сети.
        :return: Полный адрес узла сети.
        """
        return obj.get_full_address()

    get_full_address.short_description = 'Полный адрес'

    def get_supplier_link(self, obj):
        """
        Получение ссылки на поставщика узла.

        :param obj: Объект узла сети.
        :return: HTML-ссылка на страницу редактирования поставщика, если он существует, иначе '-' (дефис).
        """

        if obj.supplier:
            link = reverse("admin:network_networknode_change", args=[obj.supplier.pk])

            return format_html('<a href="{}">{}</a>', link, obj.supplier.name)
        else:
            return '-'

    get_supplier_link.short_description = 'Поставщик'

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
