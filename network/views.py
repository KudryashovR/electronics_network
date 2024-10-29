from rest_framework import viewsets, filters

from network.models import NetworkNode, Product
from network.permissions import IsStaff
from network.serializers import NetworkNodeSerializer, ProductSerializer


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с моделью NetworkNode.

    Этот ViewSet предоставляет стандартные операции CRUD (создание, чтение, обновление, удаление) для модели
    NetworkNode. Использует сериализатор NetworkNodeSerializer и фильтр SearchFilter для поиска по полю 'country'.
    Доступ ограничен пользователями с правами сотрудников.
    """

    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['country']
    permission_classes = [IsStaff]


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с моделью Product.

    Этот ViewSet предоставляет стандартные операции CRUD (создание, чтение, обновление, удаление) для модели Product.
    Использует сериализатор ProductSerializer. Доступ ограничен пользователями с правами сотрудников.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsStaff]
