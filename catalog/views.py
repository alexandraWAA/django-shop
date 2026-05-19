from django.shortcuts import render


def home(request):
    """
    Контроллер главной страницы.
    Рендерит шаблон home.html функцией render()
    """
    context = {
        'title': 'Skystore - Главная',
        'products': [
            {
                'name': 'Удобный сервис рассылок',
                'price': 140,
                'features': [
                    'Неограниченная лицензия',
                    'Поддержка',
                    'Установка на сервер',
                    'Получение обновлений'
                ]
            },
            {
                'name': 'Телеграм бот',
                'price': 100,
                'features': [
                    'Готовый код',
                    'Документация',
                    'Поддержка 24/7',
                    'Обновления 1 год'
                ]
            },
            {
                'name': 'Веб-приложение',
                'price': 200,
                'features': [
                    'Полный исходный код',
                    'Деплой на сервер',
                    'Интеграция с БД',
                    'Бесплатные обновления'
                ]
            },
        ]
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