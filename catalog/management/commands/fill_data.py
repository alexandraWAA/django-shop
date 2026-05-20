import json
from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Category, Product


class Command(BaseCommand):
    """
    Кастомная команда для загрузки тестовых данных из фикстур
    """
    help = 'Загружает тестовые данные из фикстур в базу данных'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fixtures',
            action='store_true',
            help='Загрузить данные из файлов фикстур'
        )
        parser.add_argument(
            '--sample',
            action='store_true',
            help='Создать примеры данных программно'
        )

    def handle(self, *args, **options):
        # Предварительное удаление существующих данных
        self.stdout.write(self.style.WARNING('Удаление существующих данных...'))

        # Получаем количество удаленных объектов
        products_count = Product.objects.count()
        categories_count = Category.objects.count()

        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write(self.style.SUCCESS(
            f'Удалено: {products_count} продуктов, {categories_count} категорий'
        ))

        if options['fixtures']:
            self.load_from_fixtures()
        elif options['sample']:
            self.create_sample_data()
        else:
            # По умолчанию загружаем из фикстур
            self.load_from_fixtures()

    def load_from_fixtures(self):
        """Загрузка данных из файлов фикстур"""
        self.stdout.write('Загрузка данных из фикстур...')

        fixture_dir = Path(__file__).resolve().parent.parent.parent / 'fixtures'

        try:
            # Загрузка категорий
            categories_fixture = fixture_dir / 'categories.json'
            if categories_fixture.exists():
                call_command('loaddata', str(categories_fixture), verbosity=0)
                self.stdout.write(self.style.SUCCESS('✓ Категории загружены'))
            else:
                self.stdout.write(self.style.WARNING('⚠ Файл categories.json не найден'))

            # Загрузка продуктов
            products_fixture = fixture_dir / 'products.json'
            if products_fixture.exists():
                call_command('loaddata', str(products_fixture), verbosity=0)
                self.stdout.write(self.style.SUCCESS('✓ Продукты загружены'))
            else:
                self.stdout.write(self.style.WARNING('⚠ Файл products.json не найден'))

            # Вывод статистики
            self.stdout.write(self.style.SUCCESS(
                f'✅ Данные успешно загружены!\n'
                f'   Категорий: {Category.objects.count()}\n'
                f'   Продуктов: {Product.objects.count()}'
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Ошибка загрузки: {e}'))

    def create_sample_data(self):
        """Создание примеров данных программно"""
        self.stdout.write('Создание примеров данных программно...')

        # Создание категорий
        categories_data = [
            {'name': 'Электроника', 'description': 'Смартфоны, ноутбуки, планшеты и другая техника'},
            {'name': 'Одежда', 'description': 'Мужская, женская и детская одежда'},
            {'name': 'Дом и сад', 'description': 'Товары для дома, сада и дачи'},
            {'name': 'Спорт', 'description': 'Спортивный инвентарь и экипировка'},
            {'name': 'Книги', 'description': 'Художественная и учебная литература'},
        ]

        created_categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            created_categories.append(category)
            self.stdout.write(f'  ✓ Создана категория: {category.name}')

        # Создание продуктов
        products_data = [
            {'name': 'iPhone 15 Pro', 'description': 'Флагманский смартфон Apple с процессором A17 Pro',
             'price': 999.00, 'category': 'Электроника'},
            {'name': 'Samsung Galaxy S24', 'description': 'Мощный Android-смартфон с искусственным интеллектом',
             'price': 899.00, 'category': 'Электроника'},
            {'name': 'MacBook Pro 14', 'description': 'Ноутбук для профессионалов с чипом M3', 'price': 1999.00,
             'category': 'Электроника'},
            {'name': 'Джинсы классические', 'description': 'Удобные джинсы из качественного хлопка', 'price': 79.99,
             'category': 'Одежда'},
            {'name': 'Футболка хлопковая', 'description': 'Мягкая футболка из 100% хлопка', 'price': 24.99,
             'category': 'Одежда'},
            {'name': 'Набор садовых инструментов', 'description': 'Комплект из 5 инструментов для сада', 'price': 49.99,
             'category': 'Дом и сад'},
            {'name': 'Беговая дорожка', 'description': 'Электрическая беговая дорожка для дома', 'price': 499.00,
             'category': 'Спорт'},
            {'name': 'Python. Полное руководство', 'description': 'Книга по программированию на Python', 'price': 89.99,
             'category': 'Книги'},
        ]

        for prod_data in products_data:
            try:
                category = Category.objects.get(name=prod_data['category'])
                product = Product.objects.create(
                    name=prod_data['name'],
                    description=prod_data['description'],
                    price=prod_data['price'],
                    category=category
                )
                self.stdout.write(f'  ✓ Создан продукт: {product}')
            except Category.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  ⚠ Категория "{prod_data["category"]}" не найдена'))

        # Вывод статистики
        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Примеры данных успешно созданы!\n'
            f'   Категорий: {Category.objects.count()}\n'
            f'   Продуктов: {Product.objects.count()}'
        ))