from django.contrib import admin
from catalog.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Настройка отображения категорий в админке
    """
    list_display = ('id', 'name', 'description')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    ordering = ('id',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Настройка отображения продуктов в админке
    """
    list_display = ('id', 'name', 'price', 'category', 'created_at')
    list_display_links = ('id', 'name')
    list_filter = ('category', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_editable = ('price',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'image', 'category', 'price')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )