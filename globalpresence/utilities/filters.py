from django_filters import rest_framework as filters
from ..models import GlobalPresence, Country

# Custom filter to allow multiple values
class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass

class GlobalPresenceFilter(filters.FilterSet):
    # country = CharInFilter(field_name='country', lookup_expr='in')
    country = CharInFilter(field_name='country__id', lookup_expr='in')

    class Meta:
        model = GlobalPresence
        fields = ['country']
