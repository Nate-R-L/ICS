# auctions/management/commands/import_coins.py

import csv
from django.core.management.base import BaseCommand
from auctions.models import Product
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Import coins from a CSV file'

    def handle(self, *args, **kwargs):
        with open('coins.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            products = []
            for row in reader:
                product = Product(
                    name=row['name'],
                    description=row['description'],
                    starting_bid=float(row['starting_bid']),
                    current_bid=float(row['current_bid']),
                    end_date=timezone.now() + timedelta(days=int(row['end_days'])),
                    picture_link = 'static/images/IMG_3479.png'
                )
                products.append(product)

            Product.objects.bulk_create(products)
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(products)} coin products.'))
