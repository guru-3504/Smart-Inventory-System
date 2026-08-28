from django.core.management.base import BaseCommand
from inventory.models import Category, Supplier, Product


class Command(BaseCommand):
    help = 'Seed the database with sample inventory data'

    def handle(self, *args, **kwargs):
        electronics = Category.objects.get_or_create(name='Electronics', description='Electronic gadgets and devices')[0]
        groceries = Category.objects.get_or_create(name='Groceries', description='Daily food and household items')[0]
        clothing = Category.objects.get_or_create(name='Clothing', description='Apparel and accessories')[0]

        tech_supply = Supplier.objects.get_or_create(
            name='TechSupply Co.',
            defaults={'email': 'tech@example.com', 'phone': '9876543210', 'address': '123 Tech Street, Bangalore'}
        )[0]
        fresh_mart = Supplier.objects.get_or_create(
            name='FreshMart Distributors',
            defaults={'email': 'fresh@example.com', 'phone': '9876501234', 'address': '456 Market Road, Chennai'}
        )[0]
        fashion_hub = Supplier.objects.get_or_create(
            name='Fashion Hub Wholesale',
            defaults={'email': 'fashion@example.com', 'phone': '9876512345', 'address': '789 Fashion Ave, Mumbai'}
        )[0]

        products_data = [
            {'name': 'Wireless Mouse', 'sku': 'ELEC-001', 'category': electronics, 'supplier': tech_supply, 'price': 599, 'quantity': 45, 'low_stock_threshold': 10},
            {'name': 'USB-C Cable', 'sku': 'ELEC-002', 'category': electronics, 'supplier': tech_supply, 'price': 199, 'quantity': 8, 'low_stock_threshold': 15},
            {'name': 'Bluetooth Headphones', 'sku': 'ELEC-003', 'category': electronics, 'supplier': tech_supply, 'price': 1499, 'quantity': 5, 'low_stock_threshold': 5},
            {'name': 'Basmati Rice 5kg', 'sku': 'GROC-001', 'category': groceries, 'supplier': fresh_mart, 'price': 450, 'quantity': 60, 'low_stock_threshold': 20},
            {'name': 'Cooking Oil 1L', 'sku': 'GROC-002', 'category': groceries, 'supplier': fresh_mart, 'price': 180, 'quantity': 5, 'low_stock_threshold': 10},
            {'name': 'Cotton T-Shirt', 'sku': 'CLTH-001', 'category': clothing, 'supplier': fashion_hub, 'price': 399, 'quantity': 30, 'low_stock_threshold': 8},
            {'name': 'Denim Jeans', 'sku': 'CLTH-002', 'category': clothing, 'supplier': fashion_hub, 'price': 999, 'quantity': 3, 'low_stock_threshold': 5},
        ]

        for data in products_data:
            Product.objects.get_or_create(sku=data['sku'], defaults=data)

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))