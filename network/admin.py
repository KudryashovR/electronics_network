from django.contrib import admin

from network.models import NetworkNode


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'get_full_address', 'debt', 'created_at']
    search_fields = ['name', 'city']
    list_filter = ['city']

    get_full_address = lambda self, obj: obj.get_full_address()
    get_full_address.short_description = 'Полный адрес'

    actions = ['clear_debt']

    @admin.action(description='Очистить задолжность')
    def crear_debt(self, request, queryset):
        queryset.update(debt=0.00)
