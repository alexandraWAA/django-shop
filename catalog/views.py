from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from catalog.models import Product, Category
from catalog.forms import ProductForm


class HomeListView(ListView):
    """
    Главная страница со списком товаров
    """
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        return Product.objects.select_related('category').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Skystore - Главная'
        context['categories'] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    """
    Детальная страница товара
    """
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        if self.object.category:
            context['similar_products'] = self.object.category.products.exclude(
                id=self.object.id
            )[:3]
        context['categories'] = Category.objects.all()
        return context


class ProductCreateView(CreateView):
    """
    Создание нового товара
    """
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
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


class ProductUpdateView(UpdateView):
    """
    Редактирование товара
    """
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

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


class ProductDeleteView(DeleteView):
    """
    Удаление товара
    """
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(request, f'✅ Товар "{obj.name}" успешно удален!')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ContactsView(TemplateView):
    """
    Страница контактов
    """
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
    Товары по категории
    """
    model = Product
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        self.category = Category.objects.get(pk=self.kwargs['pk'])
        return self.category.products.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['title'] = f'Категория: {self.category.name}'
        context['categories'] = Category.objects.all()
        return context