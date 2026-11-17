from django.test import TestCase
from .models import Product


class ProductModelTest(TestCase):
    def test_product_string_representation(self):
        product = Product(name="Test item", description="Example", price="100.00")
        self.assertEqual(str(product), "Test item")
