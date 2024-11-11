# blog/filters.py
import django_filters
import re
from django.db.models import Q
from ..models import Blog, BlogCategory, BlogTags
from django_filters import rest_framework as filters
from rest_framework.exceptions import ValidationError

class BlogFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(method='filter_by_author')
    category = django_filters.ModelMultipleChoiceFilter(
        field_name="category",
        queryset=BlogCategory.objects.all(),
        to_field_name="id",
    )
    tags = django_filters.CharFilter(method='filter_by_tags')
    created_date_gte = django_filters.DateFilter(
        field_name='created_at', lookup_expr='gte', label='Created Date (From)'
    )
    created_date_lte = django_filters.DateFilter(
        field_name='created_at', lookup_expr='lte', label='Created Date (To)'
    )

    class Meta:
        model = Blog
        fields = {
            'title': ['exact', 'icontains'],
            'excerpt': ['icontains'],
            'status': ['exact'],
            'position': ['exact', 'gte', 'lte']
        }

    def filter_by_author(self, queryset, name, value):
        if value:
            return queryset.filter(Q(author__icontains=value) | Q(meta_author__icontains=value))
        return queryset

    def filter_by_tags(self, queryset, name, value):
        if value:
            tags = value.split(',') if ',' in value else [value]
            queryset = queryset.filter(tags__name__in=tags).distinct()
        return queryset
