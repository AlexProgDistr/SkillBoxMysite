from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Product, ProductImage, Order


class ProductImageSerializer(serializers.ModelSerializer):
    """Сериализатор для галереи картинок продукта"""
    class Meta:
        model = ProductImage
        fields = ("image",)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя"""
    class Meta:
        model = User
        fields = ("username",)


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для продукта"""
    images = ProductImageSerializer(many=True, read_only=True)
    created_by = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Product
        fields = ("pk", "name", "description", "price", "discount", "created_at", "archived", "created_by", "preview", "images")



class ProductSerializerFromOrder(serializers.ModelSerializer):
    """Сериализатор для отображения продукта в ордере """
    class Meta:
        model = Product
        fields = ("pk", "name",)


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор для ордера"""
    user = UserSerializer(many=False, read_only=True)
    products = ProductSerializerFromOrder(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ("delivery_address", "promocode", "created_at", "user", "products")