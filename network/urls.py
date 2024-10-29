from django.urls import path, include
from rest_framework.routers import DefaultRouter

from network.apps import NetworkConfig
from network.views import NetworkNodeViewSet, ProductViewSet

app_name = NetworkConfig.name

router = DefaultRouter()
router.register(r'nodes', NetworkNodeViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
