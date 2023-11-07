
import django_filters

from blog.models import Article

class ArticleFilter(django_filters.FilterSet):
    q=django_filters.CharFilter(field_name='title',lookup_expr='icontains')

    class Meta:
        model=Article
        fields=['title','status']
