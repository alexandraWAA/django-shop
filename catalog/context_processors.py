# catalog/context_processors.py
from catalog.models import Category

def categories_processor(request):
    """Контекстный процессор для передачи категорий во все шаблоны"""
    return {
        'categories': Category.objects.all()
    }