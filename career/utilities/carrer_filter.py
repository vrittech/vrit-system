import django_filters
from django_filters import rest_framework as filters
from ..models import Career


class CareerFilter(filters.FilterSet):
    experience_level = filters.CharFilter(field_name='experience_level__level_name', lookup_expr='icontains')
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    is_show = filters.BooleanFilter(field_name='is_show')
    enable_auto_expiration = filters.BooleanFilter(field_name='enable_auto_expiration')
    created_at = filters.DateFromToRangeFilter(field_name='created_at')

    class Meta:
        model = Career
        fields = ['experience_level', 'title', 'is_show', 'enable_auto_expiration', 'created_at']
