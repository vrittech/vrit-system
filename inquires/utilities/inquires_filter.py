from django_filters import rest_framework as filters
from ..models import Inquires

# Custom filter to allow multiple selections for numeric fields
class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass

class InquiresFilter(filters.FilterSet):
    services = NumberInFilter(field_name='services', lookup_expr='in')
    project_plan = NumberInFilter(field_name='project_plan__id', lookup_expr='in')
    # created_at = filters.DateFromToRangeFilter(field_name='created_at')

    class Meta:
        model = Inquires
        fields = ['services', 'project_plan']
