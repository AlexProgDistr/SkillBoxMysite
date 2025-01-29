"""Представление моделей на страницах сайта."""

from django.views.generic import ListView

from .models import Article


class ArticleListView(ListView):
    """Отображение списка статей."""

    template_name = 'shopapp/article_list.html'
    context_object_name = 'articles'
    queryset = Article.objects.all()

    def get_queryset(self):
        """Оптимизация запросов в БД."""
        return (self.queryset
                .defer('content', 'author__bio', )
                .select_related('author')
                .select_related('category')
                .prefetch_related('tags'))
