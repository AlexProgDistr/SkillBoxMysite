import logging
from timeit import default_timer

from django.contrib.auth.models import Group, User
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, reverse
from django.core.cache import cache
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,View
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404

from .models import Product, Order
from .forms import ProductForm, OrderForm


log = logging.getLogger(__name__)

# Create your views here.
def shop_index(request: HttpRequest)-> render:
    products = [
        ('Laptop', 1999),
        ('Desktop', 2999),
        ('Smartphone', 999),
    ]
    context = {
        'time_running': default_timer(),
        'products': products,
    }
    return render(request, 'shopapp/shop-index.html', context=context)


def groups_list(request: HttpRequest) -> render:
    context = {
        'groups': Group.objects.prefetch_related('permissions').all(),
    }
    return render(request, 'shopapp/groups-list.html', context=context)


class ProductListView(ListView):
    # model = Product
    template_name = 'shopapp/products-list.html'
    context_object_name = 'products'
    queryset = Product.objects.filter(archived=False)


class ProductDetailView(DetailView):
    template_name = 'shopapp/product-details.html'
    # model = Product
    queryset = Product.objects.prefetch_related('images').all()
    context_object_name = 'product'


class ProductCreateView(PermissionRequiredMixin, CreateView):
    """имя файла html шаблона формируется из названия модели (product)  и суффикса  (_form )"""
    permission_required = "shopapp.add_product"
    model = Product
    success_url = reverse_lazy("shopapp:products_list")
    form_class = ProductForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProductUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = "shopapp.change_product"
    model = Product
    fields = 'name', 'price', 'description', 'discount', 'preview'
    template_name_suffix = "_update_form"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.created_by == self.request.user or self.request.user.is_superuser:
            return obj
        return HttpResponseForbidden("Вы не можете редактировать этот продукт.")


    def get_success_url(self):
        log.info("Update product pk: %s", self.object.pk)
        return reverse("shopapp:product_detail", kwargs={"pk": self.object.pk})



class ProductDeleteView(DeleteView):
    """имя файла html шаблона формируется из названия модели (product)  и суффикса  (_confirm_delete )"""
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrderListView(ListView):
    model = Order
    template_name = 'shopapp/orders-list.html'
    context_object_name = 'orders'


class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "shopapp.view_order"
    template_name = 'shopapp/order-detail.html'
    model = Order
    context_object_name = 'order'


class OrderCreateView(CreateView):
    """имя файла html шаблона формируется из названия модели (order)  и суффикса  (_form )"""
    model = Order
    success_url = reverse_lazy("shopapp:orders_list")
    form_class = OrderForm


class OrderDeleteView(DeleteView):
    """имя файла html шаблона формируется из названия модели (order)  и суффикса  (_confirm_delete )"""
    model = Order
    success_url = reverse_lazy("shopapp:orders_list")

class OrderUpdateView(UpdateView):
    """имя файла html шаблона формируется из названия модели (order)  и суффикса  указанного в параметре template_name_suffix"""
    model = Order
    fields = 'delivery_address', 'promocode', 'user', 'products'
    template_name_suffix = "_update_form"
    # success_url = reverse_lazy("shopapp:products_list")

    def get_success_url(self):
        return reverse("shopapp:order_detail", kwargs={"pk": self.object.pk})


class OrdersDataExportView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.select_related('user').prefetch_related('products').order_by("pk").all()
        orders_data = [
            {
                "pk": order.pk,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,
                "user": order.user.pk,
                "products": [product.pk for product in order.products.all()]
            }
            for order in orders
        ]
        return JsonResponse({"orders": orders_data})


# class ProductViewSet(ModelViewSet):
#     queryset = Product.objects.select_related('created_by').prefetch_related('images').all()
#     serializer_class = ProductSerializer
#     filterset_fields = [
#         "name",
#         "description",
#         "price",
#         "discount",
#         "archived",
#     ]
#
#     filter_backends = [
#         SearchFilter,
#         DjangoFilterBackend,
#         OrderingFilter
#     ]
#
#     search_fields = ["name", "description"]
#
#     ordering_fields = [
#         "pk",
#         "name",
#         "price",
#         "discount",
#     ]
#
#     # def get_queryset(self):
#     #     return self.queryset.prefetch_related('images')
#
#
# class OrderViewSet(ModelViewSet):
#     queryset = Order.objects.prefetch_related('products').all()
#     serializer_class = OrderSerializer
#
#     filterset_fields = [
#         "delivery_address",
#         "promocode",
#         "user",
#     ]
#
#     filter_backends = [
#         SearchFilter,
#         DjangoFilterBackend,
#         OrderingFilter
#     ]
#
#     search_fields = ["delivery_address", "user"]
#
#     ordering_fields = [
#         "pk",
#         "promocode",
#         "delivery_address",
#     ]


class LatestProductsFeed(Feed):
    title = "New products(latest)"
    description = "Updates on changes and additions products"
    link = reverse_lazy("shopapp:products_list")

    def items(self):
        return Product.objects.filter(archived=False).order_by("-created_by")[:5]

    def item_title(self, item: Product):
        return item.name

    def item_description(self, item: Product):
        return item.description[:200]


class UserOrdersListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Order
    template_name = 'shopapp/orders_user.html'
    context_object_name = 'orders'


    def get_queryset(self):
        """Получение id user'a по которому производиться запрос"""
        user_id = self.kwargs['user_id']
        self.onwer = get_object_or_404(User, pk=user_id)
        return Order.objects.filter(user=self.onwer).select_related('user').prefetch_related('products').order_by("pk").all()

    def get_context_data(self, **kwargs):
        """Добавление id user'a в контекст шаблона"""
        context = super().get_context_data(**kwargs)
        context['user'] = self.onwer
        return context

    def test_func(self):
        """Просматривать список ордеров могут только суперпользователь, администраторы
            и авторы заказов
        """
        return (self.request.user.is_superuser
                or self.request.user.is_staff
                or self.request.user.pk == self.kwargs['user_id'])



class OrdersExportView(View):
    def get(self, request: HttpRequest, user_id) -> HttpResponse|JsonResponse:
        cache_key = f"user_{user_id}"
        orders_data = cache.get(cache_key)
        if orders_data is None:
            try:
                user = User.objects.get(pk=user_id)
            except:
                return HttpResponse("User not found", status=404)

            orders = Order.objects.filter(user=user).select_related('user').prefetch_related('products').order_by("pk").all()
            orders_data = [
                {
                    "pk": order.pk,
                    "user": order.user.pk,
                    "delivery_address": order.delivery_address,
                    "promocode": order.promocode,
                    "products": [product.pk for product in order.products.all()]
                }
                for order in orders
            ]
            cache.set(cache_key, orders_data, 120)
        return JsonResponse({"orders": orders_data})
