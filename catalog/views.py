from django.shortcuts import render
from catalog.models import Product


def home(request):
    """
    Контроллер главной страницы.
    Рендерит шаблон home.html функцией render()
    """
    # * Дополнительное задание: выборка последних 5 созданных продуктов
    recent_products = Product.objects.all().order_by('-created_at')[:5]

    # Вывод в консоль последних 5 продуктов
    print("\n" + "=" * 60)
    print("📦 ПОСЛЕДНИЕ 5 СОЗДАННЫХ ПРОДУКТОВ:")
    print("=" * 60)
    for idx, product in enumerate(recent_products, 1):
        print(
            f"{idx}. {product.name} - ${product.price} (Категория: {product.category.name if product.category else 'Без категории'})")
    print("=" * 60 + "\n")

    context = {
        'title': 'Skystore - Главная',
        'products': recent_products,
    }
    return render(request, 'catalog/home.html', context)


def contacts(request):
    """
    Контроллер страницы контактов.
    Рендерит шаблон contacts.html функцией render()
    + обработка POST-запроса (дополнительное задание)
    """
    message_sent = False

    if request.method == 'POST':
        # Получаем данные из формы
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')

        # Выводим в консоль для проверки
        print("\n" + "=" * 50)
        print("📬 Получены данные от пользователя:")
        print(f"   Имя: {name}")
        print(f"   Телефон: {phone}")
        print(f"   Email: {email}")
        print(f"   Сообщение: {message}")
        print("=" * 50 + "\n")

        message_sent = True

    context = {
        'title': 'Skystore - Контакты',
        'message_sent': message_sent,
    }
    return render(request, 'catalog/contacts.html', context)