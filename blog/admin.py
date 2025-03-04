from django.contrib import admin
from .models import Category, BlogPost

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created_at', 'is_draft')
    list_filter = ('category', 'is_draft', 'created_at')
    search_fields = ('title', 'summary', 'content')
    date_hierarchy = 'created_at'