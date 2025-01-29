from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _



def product_preview_directory_path(instance: "Product", filename: str) -> str:
    """Определяет место хранения файла картинки-превью"""
    return f"products/product_{instance.pk}/preview/{filename}"


class Product(models.Model):

    class Meta:
        ordering =['name', 'price']
        verbose_name = _('product')
        verbose_name_plural = _('products')

    name = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, default=1)
    preview = models.ImageField(null=True, blank=True, upload_to=product_preview_directory_path)


    def __str__(self) -> str:
        return f"Product: pk={self.pk}, name={self.name!r}"

    def get_absolute_url(self):
        return reverse("shopapp:product_detail", kwargs={"pk": self.pk})


def product_images_directory_path(instance: "ProductImage", filename: str) -> str:
    """Определяет место хранения файлов картинок продукта"""
    return f"products/product_{instance.product.pk}/images/{filename}"


class ProductImage(models.Model):
    """Класс для хранения изображений для продуктов"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(null=True, blank=True, upload_to=product_images_directory_path)
    description = models.CharField(max_length=200, null=False, blank=True)


class Order(models.Model):
    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    delivery_address = models.TextField(null=False, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name='orders')
