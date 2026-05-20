from django.urls import path
from catalog import views

app_name = 'catalog'

urlpatterns = [
    # Главная страница
    path('', views.home, name='home'),
    path('home/', views.home, name='home_redirect'),

    # Страница контактов
    path('contacts/', views.contacts, name='contacts'),

    # Детальная страница товара (URL вида /products/int:pk/)
    path('products/<int:pk>/', views.product_detail, name='product_detail'),

    # Добавление товара (дополнительное задание)
    path('products/create/', views.product_create, name='product_create'),

    # Товары по категории
    path('category/<int:pk>/', views.category_products, name='category_products'),
]