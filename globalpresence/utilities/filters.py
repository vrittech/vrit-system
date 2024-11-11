from django_filters import rest_framework as filters
from ..models import GlobalPresence, Country

# Custom filter to allow multiple values
class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass

class GlobalPresenceFilter(filters.FilterSet):
    global_presence = CharInFilter(field_name='global_presence', lookup_expr='in')
    country = CharInFilter(field_name='country__id', lookup_expr='in')  # Filter by multiple countries by ID

    class Meta:
        model = GlobalPresence
        fields = ['global_presence', 'country']
