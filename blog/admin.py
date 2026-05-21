from django.contrib import admin
from blog.models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'is_published', 'views_count')
    list_display_links = ('id', 'title')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    readonly_fields = ('views_count', 'created_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'content', 'preview', 'is_published')
        }),
        ('Статистика', {
            'fields': ('views_count', 'created_at'),
            'classes': ('collapse',)
        }),
    )