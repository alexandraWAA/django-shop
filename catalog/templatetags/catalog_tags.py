from django import template
from catalog.models import Category

register = template.Library()


@register.simple_tag
def get_categories():
    """Возвращает все категории для использования в шаблонах"""
    return Category.objects.all()


@register.inclusion_tag('catalog/includes/categories_menu.html')
def show_categories():
    """Возвращает шаблон с меню категорий"""
    return {'categories': Category.objects.all()}