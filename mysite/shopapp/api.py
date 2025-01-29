
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import ProductSerializer, OrderSerializer
from .models import Product, Order


class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product.
    Полный GRUD для сущностей товара
    """
    queryset = Product.objects.select_related('created_by').prefetch_related('images').all()
    serializer_class = ProductSerializer
    filterset_fields = [
        "name",
        "description",
        "price",
        "discount",
        "archived",
    ]

    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter
    ]

    search_fields = ["name", "description"]

    ordering_fields = [
        "pk",
        "name",
        "price",
        "discount",
    ]


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.prefetch_related('products').all()
    serializer_class = OrderSerializer

    filterset_fields = [
        "delivery_address",
        "promocode",
        "user",
    ]

    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter
    ]

    search_fields = ["delivery_address", "user"]

    ordering_fields = [
        "pk",
        "promocode",
        "delivery_address",
    ]
