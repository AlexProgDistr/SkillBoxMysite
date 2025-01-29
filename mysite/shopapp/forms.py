from django import  forms


from .models import Product, Order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = 'name', 'price', 'description', 'discount', 'preview'



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = 'delivery_address', 'promocode', 'user', 'products'


class CSVImportForm(forms.Form):
    """Форма для импорта данных."""

    csv_file = forms.FileField()