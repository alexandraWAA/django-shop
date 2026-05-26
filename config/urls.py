from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Приложение catalog
    path('', include('catalog.urls')),
    # Приложение blog
    path('blogs/', include('blog.urls')),
    # Приложение users
    path('users/', include('users.urls')),
]

# Добавляем поддержку медиафайлов в режиме отладки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)