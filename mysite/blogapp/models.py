"""Описание таблиц БД в виде классов."""

from django.db import models


class Author(models.Model):
    """Модель описывает авторов статей.

    name: Имя автора
    bio:  Биография автора
    """

    class Meta:
        """Определяет поведения модели в программе."""

        ordering = ['name']
        verbose_name = 'author'
        verbose_name_plural = 'authors'

    name = models.CharField(max_length=100, db_index=True)
    bio = models.TextField(null=False, blank=True)


class Category(models.Model):
    """Модель описывает категории статей.

    name: Наименование категориии
    """

    class Meta:
        """Определяет поведения модели в программе."""

        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    name = models.CharField(max_length=100, db_index=True)


class Tag(models.Model):
    """Модель описывает теги статей.

    name: Наименование тега
    """

    class Meta:
        """Определяет поведения модели в программе."""

        ordering = ['name']
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    name = models.CharField(max_length=100, db_index=True)


class Article(models.Model):
    """Модель описывает даанные статьи.

    title: Заголовок
    content: Содержание
    pub_date: Дата публикации
    author: Автор
    category: Категория статьи
    tags: Теги статьи
    """

    class Meta:
        """Определяет поведения модели в программе."""

        verbose_name = 'articte'
        verbose_name_plural = 'articles'

    title = models.CharField(max_length=200, db_index=True)
    content = models.TextField(null=False, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
