from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


def send_welcome_email(user_email, user_name):
    """
    Отправка приветственного письма пользователю после регистрации
    """
    subject = 'Добро пожаловать в Skystore!'

    # HTML версия письма
    html_message = render_to_string('users/welcome_email.html', {
        'user_name': user_name,
        'site_url': 'http://localhost:8000',
    })

    # Текстовая версия письма
    plain_message = f"""
    Здравствуйте, {user_name}!

    Добро пожаловать в Skystore - ваш любимый интернет-магазин!

    Мы рады видеть вас среди наших покупателей.

    С уважением,
    Команда Skystore
    """

    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Ошибка отправки email: {e}")
        return False