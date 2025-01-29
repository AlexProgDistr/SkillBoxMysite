"""Представление моделей в админ панели."""


from django.contrib import admin
from django.http import HttpRequest

from .models import Author, Category, Tag, Article


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Представление модели  Author в админ панели."""

    list_display = ['pk', 'name', 'bio_short']
    list_display_links = ['pk', 'name']
    ordering = ['name', 'pk']
    search_fields = ['name', 'bio']

    def bio_short(self, obj: Author) -> str:
        """Краткое отображение биографии автора."""
        if len(obj.bio) < 48:
            return obj.bio
        return obj.bio[0:48] + '...'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Представление модели  Category в админ панели."""

    list_display = ['pk', 'name']
    list_display_links = ['pk', 'name']
    ordering = ['name', 'pk']
    search_fields = ['name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Представление модели  Tag в админ панели."""

    list_display = ['pk', 'name']
    list_display_links = ['pk', 'name']
    ordering = ['name', 'pk']
    search_fields = ['name']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Представление модели  Article в админ панели."""

    list_display = [
        'pk', 'title',
        'content_short',
        'pub_date',
        'author_name',
        'category_name'
    ]
    list_display_links = ['pk', 'title']
    ordering = ['title', 'pk']
    search_fields = ['title', 'pub_date', 'category', ]

    def content_short(self, obj: Article) -> str:
        """Краткое отображение содержания."""
        if len(obj.content) < 48:
            return obj.content
        return obj.content[0:48] + '...'

    def author_name(self, obj: Author) -> str:
        """Отображение имени автора в таблице."""
        return obj.author.name

    def category_name(self, obj: Category) -> str:
        """Отображение категории в таблице."""
        return obj.category.name

    def get_queryset(self, request: HttpRequest):
        """Подгрузка имен авторов и категорий."""
        return (Article.objects.select_related('author').select_related('category'))
