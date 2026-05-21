from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from catalog.models import Product, Category
from catalog.forms import ProductForm


class HomeListView(ListView):
    """
    Контроллер главной страницы со списком товаров (CBV)
    """
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        """Возвращает все продукты с предзагрузкой категории"""
        return Product.objects.select_related('category').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Skystore - Главная'
        return context


class ProductDetailView(DetailView):
    """
    Контроллер страницы подробной информации о товаре (CBV)
    URL вида /products/int:pk/
    """
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        # Похожие товары из той же категории
        if self.object.category:
            context['similar_products'] = self.object.category.products.exclude(
                id=self.object.id
            )[:3]
        return context


class ProductCreateView(CreateView):
    """
    Контроллер для добавления нового товара (CBV)
    """
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_create.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        """Добавляем сообщение об успехе"""
        response = super().form_valid(form)
        messages.success(self.request, f'Товар "{self.object.name}" успешно добавлен!')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить товар'
        return context


class ContactsView(TemplateView):
    """
    Контроллер страницы контактов (CBV с TemplateView)
    """
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Skystore - Контакты'
        context['message_sent'] = False
        return context

    def post(self, request, *args, **kwargs):
        """Обработка POST-запроса из формы"""
        context = self.get_context_data(**kwargs)

        # Получаем данные из формы
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')

        # Выводим в консоль
        print("\n" + "=" * 50)
        print("📬 Получены данные от пользователя:")
        print(f"   Имя: {name}")
        print(f"   Телефон: {phone}")
        print(f"   Email: {email}")
        print(f"   Сообщение: {message}")
        print("=" * 50 + "\n")

        context['message_sent'] = True
        return self.render_to_response(context)


class CategoryProductsView(ListView):
    """
    Контроллер для отображения товаров по категории (CBV)
    """
    model = Product
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        """Фильтруем продукты по категории"""
        self.category = Category.objects.get(pk=self.kwargs['pk'])
        return self.category.products.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['title'] = f'Категория: {self.category.name}'
        return context