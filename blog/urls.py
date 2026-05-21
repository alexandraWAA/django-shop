from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    # Список статей (только опубликованные)
    path('', views.BlogListView.as_view(), name='blog_list'),

    # Детальная страница статьи
    path('<int:pk>/', views.BlogDetailView.as_view(), name='blog_detail'),

    # Создание статьи
    path('create/', views.BlogCreateView.as_view(), name='blog_create'),

    # Редактирование статьи
    path('<int:pk>/update/', views.BlogUpdateView.as_view(), name='blog_update'),

    # Удаление статьи
    path('<int:pk>/delete/', views.BlogDeleteView.as_view(), name='blog_delete'),
]