import django_filters
from ..models import Forms


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass

class FormsFilter(django_filters.FilterSet):
    category = NumberInFilter(field_name="category", lookup_expr="in")
    id = NumberInFilter(field_name="id", lookup_expr="in")

    class Meta:
        model = Forms
        fields = ['id', 'category']