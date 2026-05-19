from django.urls import path
from catalog import views

app_name = 'catalog'

urlpatterns = [
    # Главная страница (контроллер на адрес / или /home/)
    path('', views.home, name='home'),
    path('home/', views.home, name='home_redirect'),
    # Страница контактов (адрес contacts/)
    path('contacts/', views.contacts, name='contacts'),
]