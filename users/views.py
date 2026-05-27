from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.core.exceptions import ValidationError
from users.forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from users.utils import send_welcome_email
from users.models import User


def register_view(request):
    """
    Регистрация пользователя
    """
    if request.user.is_authenticated:
        return redirect('catalog:home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Создание пользователя
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password1'])
                user.username = None  # Убираем username
                user.save()

                # Отправка приветственного письма
                send_welcome_email(user.email, user.first_name or user.email)

                # Автоматический вход после регистрации
                login(request, user)

                messages.success(request,
                                 f'Добро пожаловать, {user.first_name or user.email}! Регистрация успешно завершена.')
                return redirect('catalog:home')

            except Exception as e:
                messages.error(request, f'Ошибка при регистрации: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Ошибка в поле "{field}": {error}')
    else:
        form = UserRegistrationForm()

    context = {
        'title': 'Регистрация',
        'form': form,
    }
    return render(request, 'users/register.html', context)


def login_view(request):
    """
    Авторизация пользователя по email и паролю
    """
    if request.user.is_authenticated:
        return redirect('catalog:home')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Аутентификация по email
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.first_name or user.email}!')

                # Перенаправление на страницу, которую запрашивали до входа
                next_url = request.GET.get('next', 'catalog:home')
                return redirect(next_url)
            else:
                messages.error(request, 'Неверный email или пароль.')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = UserLoginForm()

    context = {
        'title': 'Вход в аккаунт',
        'form': form,
    }
    return render(request, 'users/login.html', context)


@login_required
def logout_view(request):
    """
    Выход из аккаунта
    """
    logout(request)
    messages.info(request, 'Вы вышли из аккаунта.')
    return redirect('catalog:home')


@login_required
def profile_view(request):
    """
    Просмотр профиля пользователя (дополнительное задание)
    """
    context = {
        'title': 'Мой профиль',
        'user': request.user,
    }
    return render(request, 'users/profile.html', context)


@login_required
def profile_edit_view(request):
    """
    Редактирование профиля пользователя (дополнительное задание)
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('users:profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Ошибка в поле "{field}": {error}')
    else:
        form = UserProfileForm(instance=request.user)

    context = {
        'title': 'Редактирование профиля',
        'form': form,
    }
    return render(request, 'users/profile_edit.html', context)