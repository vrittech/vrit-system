import django_filters
from ..models import Blog
from django.db.models import Q

class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass

class BlogFilter(django_filters.FilterSet):
    category = NumberInFilter(field_name="category", lookup_expr="in", method="filter_category")
    author = NumberInFilter(field_name="user", lookup_expr="in", method="filter_author")
    status = django_filters.CharFilter(
        field_name="status",
        lookup_expr="exact"
    )

    class Meta:
        model = Blog
        fields = ['id', 'category']

    def filter_category(self, queryset, name, value):
        """
        If -1 is passed, return FAQs with no category.
        Otherwise, filter by the given list of category IDs.
        """
        if value and "-1" in [str(v) for v in value]:
            return queryset.filter(Q(category__isnull=True))
        return queryset.filter(**{f"{name}__in": value})
    
    def filter_author(self, queryset, name, value):
        """
        Filter blogs by author (user) IDs.
        Example: ?author=1,2,3
        """
        return queryset.filter(user__in=value)