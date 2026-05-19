from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Подключаем URL-адреса приложения catalog
    path('', include('catalog.urls')),  # Все URL заканчиваются на /
]