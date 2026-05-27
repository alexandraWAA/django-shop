from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from catalog.models import Product, Category
from catalog.forms import ProductForm


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
    """Детальная страница товара"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        context['categories'] = Category.objects.all()
        context['can_edit'] = self.object.can_edit(self.request.user)
        context['can_delete'] = self.object.can_delete(self.request.user)
        if self.object.category:
            context['similar_products'] = self.object.category.products.filter(
                status=Product.PUBLISHED
            ).exclude(id=self.object.id)[:3]
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
        messages.success(request, f'✅ Товар "{obj.name}" успешно удален!')
        return super().delete(request, *args, **kwargs)

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
    """Товары по категории - только опубликованные"""
    model = Product
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        self.category = Category.objects.get(pk=self.kwargs['pk'])
        return self.category.products.filter(status=Product.PUBLISHED)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['title'] = f'Категория: {self.category.name}'
        context['categories'] = Category.objects.all()
        return context


# Добавляем необходимый импорт
from django.shortcuts import redirect