from django_filters import rest_framework as filters
from ..models import Inquires
from django.db.models import Q

# Custom filter to allow multiple selections for numeric fields
class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass

class InquiresFilter(filters.FilterSet):
    project_plan = NumberInFilter(field_name='project_plan__id', lookup_expr='in')
    services = NumberInFilter(field_name="services", lookup_expr="in", method="filter_services")

    class Meta:
        model = Inquires
        fields = ['services', 'project_plan']



    def filter_services(self, queryset, name, value):
        """
        If -1 is passed, return FAQs with no category.
        Otherwise, filter by the given list of category IDs.
        """
        if value and "-1" in [str(v) for v in value]:
            return queryset.filter(Q(services__isnull=True))
        return queryset.filter(**{f"{name}__in": value})


