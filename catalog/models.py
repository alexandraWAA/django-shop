from django.db import models
from django.urls import reverse
from django.conf import settings


class Category(models.Model):
    """
    Модель категории товаров
    """
    name = models.CharField(
        max_length=100,
        verbose_name='наименование',
        help_text='Введите наименование категории'
    )
    description = models.TextField(
        verbose_name='описание',
        help_text='Введите описание категории',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:category_products', args=[self.pk])


class Product(models.Model):
    """
    Модель продукта (товара)
    """
    # Статусы публикации
    DRAFT = 'draft'
    PUBLISHED = 'published'

    STATUS_CHOICES = [
        (DRAFT, 'Черновик'),
        (PUBLISHED, 'Опубликован'),
    ]

    name = models.CharField(
        max_length=200,
        verbose_name='наименование',
        help_text='Введите наименование товара'
    )
    description = models.TextField(
        verbose_name='описание',
        help_text='Введите описание товара'
    )
    image = models.ImageField(
        upload_to='products/',
        verbose_name='изображение',
        help_text='Загрузите изображение товара (JPEG, PNG, до 5 МБ)',
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name='категория',
        help_text='Выберите категорию товара'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='цена за покупку',
        help_text='Введите цену товара (должна быть больше 0)'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='дата последнего изменения'
    )

    # НОВЫЕ ПОЛЯ
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=DRAFT,
        verbose_name='статус публикации',
        help_text='Выберите статус продукта'
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name='владелец',
        help_text='Пользователь, создавший продукт'
    )

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['-created_at', 'name']

        # Кастомные права
        permissions = [
            ('can_unpublish_product', 'Может отменять публикацию продукта'),
        ]

    def __str__(self):
        return f"{self.name} (${self.price})"

    def get_absolute_url(self):
        return reverse('catalog:product_detail', args=[self.pk])

    def is_published(self):
        """Проверка, опубликован ли продукт"""
        return self.status == self.PUBLISHED

    def can_edit(self, user):
        """
        Проверка, может ли пользователь редактировать продукт
        Владелец продукта или модератор
        """
        if not user.is_authenticated:
            return False
        # Владелец продукта
        if self.owner == user:
            return True
        # Модератор
        if user.has_perm('catalog.can_unpublish_product'):
            return True
        return False

    def can_delete(self, user):
        """
        Проверка, может ли пользователь удалить продукт
        Владелец продукта или модератор
        """
        if not user.is_authenticated:
            return False
        # Модератор может удалять любые продукты
        if user.has_perm('catalog.can_unpublish_product'):
            return True
        # Владелец продукта
        if self.owner == user:
            return True
        return False