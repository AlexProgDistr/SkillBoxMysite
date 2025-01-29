from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    shop_index,
    groups_list,
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    OrderListView,
    OrderDetailView,
    OrderCreateView,
    OrderDeleteView,
    OrderUpdateView,
    OrdersDataExportView,
    LatestProductsFeed,
    UserOrdersListView,
    OrdersExportView
)

from .api import (
    ProductViewSet,
    OrderViewSet
)


app_name = 'shopapp'

routers = DefaultRouter()
routers.register("products", ProductViewSet)
routers.register("orders", OrderViewSet)

urlpatterns = [
    path('', shop_index, name='index'),
    path('groups/', groups_list, name='groups_list'),
    path('products/', ProductListView.as_view(), name='products_list'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('products/latest/feed/', LatestProductsFeed(), name='produucts_feed'),
    path('orders/', OrderListView.as_view(), name='orders_list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('orders/neworder/', OrderCreateView.as_view(), name='order_create'),
    path('orders/<int:pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),
    path('orders/<int:pk>/update/', OrderUpdateView.as_view(), name='order_update'),
    path('orders/export/', OrdersDataExportView.as_view(), name='orders_export'),
    path('api/', include(routers.urls)),

    path('users/<int:user_id>/orders/', UserOrdersListView.as_view(), name='user_order'),
    path('users/<int:user_id>/orders/export/', OrdersExportView.as_view(), name='orders_export'),
]
