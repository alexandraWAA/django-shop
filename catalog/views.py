from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from catalog.models import Product, Category
from catalog.forms import ProductForm


def home(request):
    """
    Контроллер главной страницы со списком товаров и пагинацией
    """
    # Получаем все продукты
    products_list = Product.objects.select_related('category').all()

    # Пагинация (дополнительное задание)
    paginator = Paginator(products_list, 6)  # 6 товаров на странице
    page_number = request.GET.get('page', 1)
    products = paginator.get_page(page_number)

    context = {
        'title': 'Skystore - Главная',
        'products': products,
        'paginator': paginator,
    }
    return render(request, 'catalog/home.html', context)


def product_detail(request, pk):
    """
    Контроллер страницы подробной информации о товаре
    URL вида /products/int:pk/
    """
    # Извлекаем объект через ORM
    product = get_object_or_404(Product, pk=pk)

    context = {
        'title': product.name,
        'product': product,
    }
    return render(request, 'catalog/product_detail.html', context)


def contacts(request):
    """
    Контроллер страницы контактов
    """
    message_sent = False

    if request.method == 'POST':
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')

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


def product_create(request):
    """
    Контроллер для добавления нового товара (дополнительное задание)
    """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Товар "{product.name}" успешно добавлен!')
            return redirect('catalog:product_detail', pk=product.pk)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = ProductForm()

    context = {
        'title': 'Добавить товар',
        'form': form,
    }
    return render(request, 'catalog/product_create.html', context)


def category_products(request, pk):
    """
    Контроллер для отображения товаров по категории
    """
    category = get_object_or_404(Category, pk=pk)
    products = category.products.all()

    context = {
        'title': f'Категория: {category.name}',
        'category': category,
        'products': products,
    }
    return render(request, 'catalog/category_products.html', context)