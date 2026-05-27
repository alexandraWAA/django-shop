from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Кастомная модель пользователя
    Email используется как поле для авторизации (USERNAME_FIELD)
    """
    username = None  # Удаляем поле username
    email = models.EmailField(
        _('email address'),
        unique=True,
        help_text='Введите email адрес'
    )

    # Дополнительные поля
    avatar = models.ImageField(
        upload_to='avatars/',
        verbose_name='аватар',
        blank=True,
        null=True,
        help_text='Загрузите аватар (необязательно)'
    )
    phone_number = models.CharField(
        max_length=20,
        verbose_name='номер телефона',
        blank=True,
        null=True,
        help_text='Введите номер телефона'
    )
    country = models.CharField(
        max_length=100,
        verbose_name='страна',
        blank=True,
        null=True,
        help_text='Введите страну проживания'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ['-date_joined']

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return self.email