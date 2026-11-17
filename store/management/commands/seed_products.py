from django.core.management.base import BaseCommand
from store.models import Product

class Command(BaseCommand):
    help = "Create a few sample ShopEase products if the product table is empty."

    def handle(self, *args, **options):
        if Product.objects.exists():
            self.stdout.write(self.style.WARNING("Products already exist; no sample products added."))
            return
        samples = [
            {"name": "Wireless Headphones", "description": "Comfortable wireless headphones for music, calls and everyday use.", "price": "1499.00", "category": "Electronics", "stock": 15, "image_url": "https://images.unsplash.com/photo-150 headphones"},
            {"name": "Classic Backpack", "description": "A lightweight everyday backpack with useful storage space.", "price": "999.00", "category": "Fashion", "stock": 20},
            {"name": "Smart Watch", "description": "A modern smart watch for everyday activity and notifications.", "price": "2499.00", "category": "Electronics", "stock": 10},
            {"name": "Desk Lamp", "description": "A compact desk lamp for study and work spaces.", "price": "799.00", "category": "Home", "stock": 12},
        ]
        # Omit invalid placeholder image URL; product cards show a designed placeholder instead.
        for item in samples:
            item.pop("image_url", None)
            Product.objects.create(**item)
        self.stdout.write(self.style.SUCCESS("Sample products created successfully."))
