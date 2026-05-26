from django import template
from catalog.models import Category

register = template.Library()


@register.simple_tag
def get_categories():
    """Возвращает все категории для использования в шаблонах"""
    return Category.objects.all()