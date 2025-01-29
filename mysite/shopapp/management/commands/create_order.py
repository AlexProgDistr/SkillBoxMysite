from django.contrib.auth.models import User
from django.core.management import BaseCommand

from shopapp.models import Order

class Command(BaseCommand):
    """Create orders"""

    def handle(self, *args, **options):
        self.stdout.write('Create order')
        user = User.objects.get(username='admin')
        order = Order.objects.get_or_create(
            delivery_address='Staraya Kupavna',
            promocode='SALE123',
            user=user
        )
        self.stdout.write(f'Create order {order}')
        self.stdout.write(self.style.SUCCESS('Order create OK'))