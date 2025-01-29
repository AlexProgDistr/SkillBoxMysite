from io import TextIOWrapper
from csv import DictReader

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path
from django.contrib.auth.models import User

from .models import Product, Order, ProductImage
from .admin_mixins import ExportAsCSVMixin
from .forms import CSVImportForm

@admin.action(description='Archived products')
def mark_archived(modelAdmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)

@admin.action(description='Unarchived products')
def mark_unarchived(modelAdmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


class OrderInline(admin.TabularInline):
    model = Product.orders.through

class ProductInline(admin.StackedInline):
    model = ProductImage

@admin.register(Product)
class ProductAddmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [mark_archived, mark_unarchived, 'expoort_csv',]
    inlines = [OrderInline, ProductInline]
    list_display = ['pk', 'name', 'description_short', 'price', 'discount', 'archived']
    list_display_links = ['pk', 'name']
    ordering = ['name', 'pk']
    search_fields = ['name', 'description', 'price', 'discount']
    fieldsets = [
        (None, {
            'fields': ('name', 'description'),
        }),
        ('Price options',{
            'fields': ('price', 'discount',),
        }),
        ('Images', {
            'fields': ('preview',),
        }),
        ('Extra options', {
            'fields': ('archived', ),
            'classes': ('collapse', ),
            'description': 'Extra options. Field "archived" is for soft delete',
        }),
    ]

    def description_short(self, obj:Product) -> str:
        if len(obj.description) < 48:
            return obj.description
        return obj.description[0:48] + '...'


class ProductInline(admin.TabularInline):
    model = Order.products.through

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [ProductInline, ]
    list_display = ['delivery_address', 'promocode', 'created_at', 'user_verbose']
    change_list_template = "shopapp/orders_changelist.html"


    def get_queryset(self, request: HttpRequest):
        return Order.objects.select_related('user').prefetch_related('products')

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        """Импорт заказов из файла."""

        if request.method == "GET":
            form = CSVImportForm()
            context = {
                "form": form,
            }
            return render(request=request, template_name='admin/csv_form.html', context=context)

        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request=request, template_name='admin/csv_form.html', context=context, status=400)

        csv_file = TextIOWrapper(
            form.files["csv_file"].file,
            encoding=request.encoding,
        )
        reader = DictReader(csv_file)

        for row in reader:
            products = [Product.objects.get(pk=pk) for pk in row["products"].split(";")]
            order = Order(
                delivery_address=row['delivery_address'],
                promocode=row['promocode'],
                user=User.objects.get(pk=row['user']),
            )
            order.save()
            order.products.add(*products)
            order.save()

        self.message_user(request, "CSV orders Imported")

        return redirect("..")


    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path("import-orders-csv/", self.import_csv, name="import_orders_csv"),
        ]
        return new_urls + urls

