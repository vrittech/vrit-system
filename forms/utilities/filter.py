import django_filters
from ..models import Forms
from django.db.models import Q


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass

class FormsFilter(django_filters.FilterSet):
    category = NumberInFilter(field_name="category", lookup_expr="in", method="filter_category")

    class Meta:
        model = Forms
        fields = ['id', 'category']

    def filter_category(self, queryset, name, value):
        """
        If -1 is passed, return FAQs with no category.
        Otherwise, filter by the given list of category IDs.
        """
        if value and "-1" in [str(v) for v in value]:
            return queryset.filter(Q(category__isnull=True))
        return queryset.filter(**{f"{name}__in": value})