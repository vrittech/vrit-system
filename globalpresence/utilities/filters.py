from django_filters import rest_framework as filters
from ..models import GlobalPresence

# Custom filter to allow multiple values
class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass

class GlobalPresenceFilter(filters.FilterSet):
    global_presence = CharInFilter(field_name='global_presence', lookup_expr='in')

    class Meta:
        model = GlobalPresence
        fields = ['global_presence']
