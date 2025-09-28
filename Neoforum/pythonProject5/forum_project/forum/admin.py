from django.contrib import admin
from .models import Category, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'post_count')
    search_fields = ('name', 'description')

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = 'Количество постов'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_name', 'category', 'created_at', 'is_published')
    list_filter = ('category', 'created_at', 'is_published')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'post', 'created_at', 'is_active')
    list_filter = ('created_at', 'is_active')
    search_fields = ('content', 'author_name', 'post__title')
    list_editable = ('is_active',)