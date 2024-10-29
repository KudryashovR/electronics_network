from rest_framework import viewsets, filters

from network.models import NetworkNode, Product
from network.permissions import IsStaff
from network.serializers import NetworkNodeSerializer, ProductSerializer


class NetworkNodeViewSet(viewsets.ModelViewSet):
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['country']
    permission_classes = [IsStaff]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsStaff]
