# auctions/management/commands/add_coins.py

from django.core.management.base import BaseCommand
from auctions.models import Product
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Add multiple coin products to the product list'

    def handle(self, *args, **kwargs):
        products = [
            Product(
                name=f'Coin{i}',
                description=f'Description for coin {i}',
                starting_bid=10.00 + i,
                current_bid=0.00,
                end_date=timezone.now() + timedelta(days=30),
                picture_link = 'static/images/IMG_3479.png'
            )
            for i in range(1, 3)  # Add 2 coins as an example
        ]
        Product.objects.bulk_create(products)
        self.stdout.write(self.style.SUCCESS(f'Successfully added 2 coin products.'))
