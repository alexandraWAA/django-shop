# Django Интернет-магазин

Учебный проект интернет-магазина на Django.

## 🚀 Технологии

- Python 3.11+
- Django 4.2

## 📦 Установка

```bash
# Клонирование репозитория
git clone <url-репозитория>
cd django-shop

# Создание виртуального окружения
python -m venv venv

# Активация виртуального окружения
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Применение миграций
python manage.py migrate

# Запуск сервера
python manage.py runserver