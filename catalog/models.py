from django.db import models
from django.urls import reverse


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
        help_text='Загрузите изображение товара',
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
        help_text='Введите цену товара'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='дата последнего изменения'
    )

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['-created_at', 'name']

    def __str__(self):
        return f"{self.name} (${self.price})"

    def get_absolute_url(self):
        return reverse('catalog:product_detail', args=[self.pk])

    def get_short_description(self, length=100):
        """Возвращает обрезанное описание"""
        if len(self.description) > length:
            return self.description[:length] + '...'
        return self.description