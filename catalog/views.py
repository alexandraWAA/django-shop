from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_headers
from catalog.models import Product, Category
from catalog.forms import ProductForm
from catalog.services import get_products_by_category, get_product_detail, clear_product_cache


class HomeListView(ListView):
    """Главная страница - показываем только опубликованные продукты"""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        # Показываем только опубликованные продукты
        return Product.objects.filter(status=Product.PUBLISHED).select_related('category', 'owner')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Skystore - Главная'
        context['categories'] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    """
    Детальная страница товара с кешированием
    """
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        """
        Получаем объект через сервисную функцию с кешированием
        """
        product_id = self.kwargs.get('pk')
        return get_product_detail(product_id, use_cache=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object

        if product:
            context['title'] = product.name
            context['can_edit'] = product.can_edit(self.request.user)
            context['can_delete'] = product.can_delete(self.request.user)

            if product.category:
                # Используем сервисную функцию для похожих товаров
                category_data = get_products_by_category(product.category.pk)
                if category_data:
                    similar = category_data['products'].exclude(id=product.id)[:3]
                    context['similar_products'] = similar

        context['categories'] = Category.objects.all()
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание товара - автоматически устанавливаем владельца"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')
    login_url = 'users:login'

    def form_valid(self, form):
        # Автоматически заполняем поле owner текущим пользователем
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f'✅ Товар "{self.object.name}" успешно создан!')
        return response

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'❌ Ошибка в поле "{field}": {error}')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление товара'
        context['button_text'] = 'Создать товар'
        context['categories'] = Category.objects.all()
        return context


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование товара - только владелец или модератор"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    login_url = 'users:login'

    def test_func(self):
        """Проверка прав на редактирование"""
        product = self.get_object()
        return product.can_edit(self.request.user)

    def handle_no_permission(self):
        """Обработка отсутствия прав"""
        messages.error(self.request, '❌ У вас нет прав для редактирования этого товара.')
        return redirect('catalog:product_detail', pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', args=[self.object.pk])

    def form_valid(self, form):
        response = super().form_valid(form)
        # Очищаем кеш после обновления
        clear_product_cache(self.object.pk, self.object.category.pk if self.object.category else None)
        messages.success(self.request, f'✅ Товар "{self.object.name}" успешно обновлен!')
        return response

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'❌ Ошибка в поле "{field}": {error}')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование товара'
        context['button_text'] = 'Сохранить изменения'
        context['categories'] = Category.objects.all()
        return context


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление товара - владелец или модератор"""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')
    login_url = 'users:login'

    def test_func(self):
        """Проверка прав на удаление"""
        product = self.get_object()
        return product.can_delete(self.request.user)

    def handle_no_permission(self):
        """Обработка отсутствия прав"""
        messages.error(self.request, '❌ У вас нет прав для удаления этого товара.')
        return redirect('catalog:product_detail', pk=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        category_id = obj.category.pk if obj.category else None
        result = super().delete(request, *args, **kwargs)
        # Очищаем кеш после удаления
        clear_product_cache(obj.pk, category_id)
        messages.success(request, f'✅ Товар "{obj.name}" успешно удален!')
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ContactsView(TemplateView):
    """Страница контактов"""
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Skystore - Контакты'
        context['message_sent'] = False
        context['categories'] = Category.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

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

        context['message_sent'] = True
        return self.render_to_response(context)


class CategoryProductsView(ListView):
    """
    Товары по категории с использованием сервисной функции и кеширования
    """
    model = Product
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'

    def dispatch(self, request, *args, **kwargs):
        """Получаем данные через сервисную функцию"""
        self.category_id = self.kwargs.get('pk')
        category_data = get_products_by_category(self.category_id)

        if category_data is None:
            from django.http import Http404
            raise Http404('Категория не найдена')

        self.category = category_data['category']
        self.products_queryset = category_data['products']

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Возвращаем предзагруженные продукты"""
        return self.products_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['title'] = f'Категория: {self.category.name}'
        context['categories'] = Category.objects.all()

        # Добавляем информацию о кеше для отладки
        cache_key = f'category_{self.category_id}'
        context['is_cached'] = cache.has_key(cache_key)

        return context


# Дополнительное представление для сброса кеша (для администрирования)
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
def clear_cache_view(request):
    """
    Эндпоинт для очистки кеша (только для суперпользователей)
    """
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Доступ запрещен'}, status=403)

    if request.method == 'POST':
        cache.clear()
        return JsonResponse({'message': 'Кеш успешно очищен'})

    return JsonResponse({'error': 'Метод не разрешен'}, status=405)