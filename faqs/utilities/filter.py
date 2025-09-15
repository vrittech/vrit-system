import django_filters
from ..models import Faqs


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass

class FaqsFilter(django_filters.FilterSet):
    faqs_category = NumberInFilter(field_name="faqs_category", lookup_expr="in")
    id = NumberInFilter(field_name="id", lookup_expr="in")

    class Meta:
        model = Faqs
        fields = ['id', 'faqs_category']