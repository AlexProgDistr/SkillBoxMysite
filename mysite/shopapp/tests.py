from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission

from .models import Order


class OrderDetailViewTestCase(TestCase):
    """Тестирование класса OrderDetailView """

    @classmethod
    def setUpClass(cls):
        """Создание пользователя и присвоение ему прав просмотра ордеров"""
        permission = Permission.objects.get(codename='view_order')
        cls.user = User.objects.create_user(
            username="test_user",
            password="123"
        )
        cls.user.user_permissions.add(permission)


    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        """"Логин пользователя и создание тестового ордера"""
        self.client.force_login(self.user)
        self.order = Order.objects.create(
            delivery_address="test_addres",
            promocode = "test_promo",
            user = self.user,
        )

    def tearDown(self):
        self.order.delete()

    def test_order_details(self):
        response = self.client.get(
            reverse("shopapp:order_detail", kwargs={"pk": self.order.pk}),
            HTTP_USER_AGENT='Mozilla/5.0'
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)
        self.assertEqual(response.context_data['order'].pk, self.order.pk)



class OrdersExportTestCase(TestCase):
    """Тестирование класса OrdersDataExportView"""

    fixtures = [
        "users-fixture.json",
        "products-fixture.json",
        "orders-fixture.json",
    ]

    @classmethod
    def setUpClass(cls):
        """Создание пользователя и присвоение ему прав администратора"""
        cls.user = User.objects.create_user(
            username="test_user",
            password="123"
        )
        cls.user.is_staff = True
        cls.user.save()


    def setUp(self):
        """"Логин пользователя"""
        self.client.force_login(self.user)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def test_get_orders_view(self):
        response = self.client.get(
            reverse("shopapp:orders_export"),
            HTTP_USER_AGENT='Mozilla/5.0'
        )
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.select_related('user').prefetch_related('products').order_by("pk").all()
        expected_data = [
            {
                "pk": order.pk,
                "delivery_address": order.delivery_address,
                "promocode" : order.promocode,
                "user": order.user.pk,
                "products": [product.pk for product in order.products.all()]
            }
            for order in orders
        ]
        orders_data = response.json()
        self.assertEqual(orders_data["orders"], expected_data)

