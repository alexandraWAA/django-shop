from django.db import models
from django.urls import reverse


class BlogPost(models.Model):
    """
    Модель блоговой записи
    """
    title = models.CharField(
        max_length=200,
        verbose_name='заголовок',
        help_text='Введите заголовок статьи'
    )
    content = models.TextField(
        verbose_name='содержимое',
        help_text='Введите текст статьи'
    )
    preview = models.ImageField(
        upload_to='blog_previews/',
        verbose_name='превью',
        help_text='Загрузите изображение для превью',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата создания'
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='признак публикации',
        help_text='Отметьте, чтобы опубликовать статью'
    )
    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name='количество просмотров',
        help_text='Счетчик просмотров статьи'
    )

    class Meta:
        verbose_name = 'блоговая запись'
        verbose_name_plural = 'блоговые записи'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Возвращает URL для просмотра статьи"""
        return reverse('blog:blog_detail', args=[self.pk])