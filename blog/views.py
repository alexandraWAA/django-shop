from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404
from blog.models import BlogPost
from blog.forms import BlogPostForm


class BlogListView(ListView):
    """
    Список блоговых записей (только опубликованные)
    """
    model = BlogPost
    template_name = 'blog/blog_list.html'
    context_object_name = 'blog_posts'
    paginate_by = 9

    def get_queryset(self):
        """
        Переопределяем метод get_queryset для фильтрации
        Выводим только статьи с положительным признаком публикации
        """
        return BlogPost.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Блог'
        return context


class BlogDetailView(DetailView):
    """
    Детальная страница блоговой записи
    При открытии увеличивается счетчик просмотров
    """
    model = BlogPost
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog_post'

    def get_object(self, queryset=None):
        """
        Переопределяем метод get_object для увеличения счетчика просмотров
        """
        obj = super().get_object(queryset)

        # Увеличиваем счетчик просмотров
        obj.views_count += 1
        obj.save()

        # * Дополнительное задание: поздравление при 100 просмотрах
        if obj.views_count == 100:
            print(f"\n🎉 ПОЗДРАВЛЯЮ! Статья '{obj.title}' набрала 100 просмотров!")
            # Здесь можно добавить отправку email
            # send_mail(...)

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context


class BlogCreateView(CreateView):
    """
    Создание новой блоговой записи
    """
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/blog_create.html'
    success_url = reverse_lazy('blog:blog_list')

    def form_valid(self, form):
        """Добавляем сообщение об успехе"""
        response = super().form_valid(form)
        messages.success(self.request, f'Статья "{self.object.title}" успешно создана!')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создать статью'
        context['button_text'] = 'Создать'
        return context


class BlogUpdateView(UpdateView):
    """
    Редактирование блоговой записи
    После успешного редактирования перенаправление на просмотр статьи
    """
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/blog_create.html'
    # Перенаправление после успешного редактирования
    success_url = reverse_lazy('blog:blog_list')

    def form_valid(self, form):
        """Добавляем сообщение об успехе"""
        response = super().form_valid(form)
        messages.success(self.request, f'Статья "{self.object.title}" успешно обновлена!')
        return response

    def get_success_url(self):
        """
        Перенаправляем пользователя на просмотр отредактированной статьи
        """
        return reverse_lazy('blog:blog_detail', args=[self.object.pk])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать статью'
        context['button_text'] = 'Сохранить'
        return context


class BlogDeleteView(DeleteView):
    """
    Удаление блоговой записи
    """
    model = BlogPost
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog:blog_list')

    def delete(self, request, *args, **kwargs):
        """Добавляем сообщение об успешном удалении"""
        obj = self.get_object()
        messages.success(request, f'Статья "{obj.title}" удалена')
        return super().delete(request, *args, **kwargs)