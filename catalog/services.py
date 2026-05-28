"""
Сервисные функции для работы с продуктами
"""

import logging
from django.core.cache import cache
from catalog.models import Category, Product

logger = logging.getLogger(__name__)


def get_products_by_category(category_id, use_cache=True, cache_timeout=3600):
    """
    Возвращает список всех продуктов в указанной категории.

    Args:
        category_id (int): ID категории
        use_cache (bool): Использовать ли кеширование
        cache_timeout (int): Время жизни кеша в секундах (по умолчанию 1 час)

    Returns:
        dict: Словарь с ключами 'category' и 'products'
    """
    # Ключ для кеша
    cache_key = f'category_{category_id}'

    # Пытаемся получить данные из кеша
    if use_cache:
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            logger.info(f'Данные для категории {category_id} получены из кеша')
            return cached_data

    # Если данных нет в кеше, получаем из базы данных
    logger.info(f'Данные для категории {category_id} получены из базы данных')

    try:
        category = Category.objects.prefetch_related('products').get(pk=category_id)
        products = category.products.filter(status=Product.PUBLISHED).select_related('owner')

        result = {
            'category': category,
            'products': products,
        }

        # Сохраняем в кеш
        if use_cache:
            cache.set(cache_key, result, cache_timeout)
            logger.info(f'Данные для категории {category_id} сохранены в кеш на {cache_timeout} секунд')

        return result

    except Category.DoesNotExist:
        logger.error(f'Категория с ID {category_id} не найдена')
        return None


def get_product_detail(product_id, use_cache=True, cache_timeout=3600):
    """
    Возвращает детальную информацию о продукте.

    Args:
        product_id (int): ID продукта
        use_cache (bool): Использовать ли кеширование
        cache_timeout (int): Время жизни кеша в секундах (по умолчанию 1 час)

    Returns:
        Product: Объект продукта или None
    """
    cache_key = f'product_detail_{product_id}'

    if use_cache:
        cached_product = cache.get(cache_key)
        if cached_product is not None:
            logger.info(f'Данные для продукта {product_id} получены из кеша')
            return cached_product

    try:
        product = Product.objects.select_related('category', 'owner').get(pk=product_id)

        if use_cache:
            cache.set(cache_key, product, cache_timeout)
            logger.info(f'Данные для продукта {product_id} сохранены в кеш на {cache_timeout} секунд')

        return product

    except Product.DoesNotExist:
        logger.error(f'Продукт с ID {product_id} не найден')
        return None


def clear_product_cache(product_id, category_id=None):
    """
    Очищает кеш для продукта и его категории.

    Args:
        product_id (int): ID продукта
        category_id (int, optional): ID категории
    """
    # Очищаем кеш продукта
    cache.delete(f'product_detail_{product_id}')

    # Очищаем кеш категории
    if category_id:
        cache.delete(f'category_{category_id}')

    logger.info(f'Очищен кеш для продукта {product_id} и категории {category_id}')


def get_all_categories_with_products(use_cache=True, cache_timeout=1800):
    """
    Возвращает все категории с продуктами.

    Args:
        use_cache (bool): Использовать ли кеширование
        cache_timeout (int): Время жизни кеша в секундах (по умолчанию 30 минут)

    Returns:
        QuerySet: QuerySet категорий
    """
    cache_key = 'all_categories_with_products'

    if use_cache:
        cached_categories = cache.get(cache_key)
        if cached_categories is not None:
            return cached_categories

    categories = Category.objects.prefetch_related('products').all()

    if use_cache:
        cache.set(cache_key, categories, cache_timeout)

    return categories