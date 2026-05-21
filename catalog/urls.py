from django.urls import path
from catalog import views

app_name = 'catalog'

urlpatterns = [
    # Главная страница (CBV)
    path('', views.HomeListView.as_view(), name='home'),
    path('home/', views.HomeListView.as_view(), name='home_redirect'),

    # Страница контактов (CBV)
    path('contacts/', views.ContactsView.as_view(), name='contacts'),

    # Детальная страница товара (CBV)
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),

    # Добавление товара (CBV)
    path('products/create/', views.ProductCreateView.as_view(), name='product_create'),

    # Товары по категории (CBV)
    path('category/<int:pk>/', views.CategoryProductsView.as_view(), name='category_products'),
]