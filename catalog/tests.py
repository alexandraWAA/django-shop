from django.test import TestCase
from catalog.models import Category, Product


class CategoryModelTest(TestCase):
    """Тесты для модели Category"""

    def test_category_creation(self):
        category = Category.objects.create(
            name='Тестовая категория',
            description='Описание тестовой категории'
        )
        self.assertEqual(str(category), 'Тестовая категория')
        self.assertEqual(category.name, 'Тестовая категория')


class ProductModelTest(TestCase):
    """Тесты для модели Product"""

    def setUp(self):
        self.category = Category.objects.create(
            name='Тестовая категория',
            description='Описание тестовой категории'
        )

    def test_product_creation(self):
        product = Product.objects.create(
            name='Тестовый продукт',
            description='Описание тестового продукта',
            price=99.99,
            category=self.category
        )
        self.assertEqual(str(product), 'Тестовый продукт ($99.99)')
        self.assertEqual(product.price, 99.99)