import django_filters
from ..models import Faqs
from django.db.models import Q

class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass

class FaqsFilter(django_filters.FilterSet):
    faqs_category = NumberInFilter(field_name="faqs_category", lookup_expr="in", method="filter_faqs_category")

    class Meta:
        model = Faqs
        fields = ['id', 'faqs_category']

    def filter_faqs_category(self, queryset, name, value):
        """
        If -1 is passed, return FAQs with no category.
        Otherwise, filter by the given list of category IDs.
        """
        if value and "-1" in [str(v) for v in value]:
            return queryset.filter(Q(faqs_category__isnull=True))
        return queryset.filter(**{f"{name}__in": value})