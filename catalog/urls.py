from django.urls import path
from catalog import views

app_name = 'catalog'

urlpatterns = [
    # READ - список товаров
    path('', views.HomeListView.as_view(), name='home'),
    path('home/', views.HomeListView.as_view(), name='home_redirect'),

    # READ - детальная страница
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),

    # CREATE - создание товара
    path('products/create/', views.ProductCreateView.as_view(), name='product_create'),

    # UPDATE - редактирование товара
    path('products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),

    # DELETE - удаление товара
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),

    # Страница контактов
    path('contacts/', views.ContactsView.as_view(), name='contacts'),

    # Товары по категории
    path('category/<int:pk>/', views.CategoryProductsView.as_view(), name='category_products'),
]