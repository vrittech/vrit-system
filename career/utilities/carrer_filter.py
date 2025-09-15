from datetime import timedelta
from django.utils import timezone
import django_filters
from django_filters import rest_framework as filters
from ..models import Career
from django.db.models import Q

class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass
class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass
class CareerFilter(filters.FilterSet):
    experience_level = NumberInFilter(field_name='experience_level__id', lookup_expr='in')
    career_category = NumberInFilter(field_name='career_category__id', lookup_expr='in')
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    is_show = filters.BooleanFilter(field_name='is_show')
    enable_auto_expiration = filters.BooleanFilter(field_name='enable_auto_expiration')
    duration_status = filters.CharFilter(method='filter_duration_status')

    class Meta:
        model = Career
        fields = ['experience_level', 'title', 'is_show', 'enable_auto_expiration', 'duration_status']

    def filter_duration_status(self, queryset, name, value):
        """
        duration_status values:
        - expired        → expiration_date <= now
        - expiring_soon  → expiration_date in next 7 days
        - not_expired    → expiration_date > 7 days from now
        """
        
        now = timezone.now()
        soon = now + timedelta(days=7)

        # Split input into a list of statuses
        statuses = [v.strip() for v in value.split(',') if v.strip()]
        if not statuses:
            return queryset

        q_filter = Q()
        for status in statuses:
            if status == 'expired':
                q_filter |= Q(expiration_date__isnull=False, expiration_date__lte=now)
            elif status == 'expiring_soon':
                q_filter |= Q(expiration_date__isnull=False, expiration_date__gt=now, expiration_date__lte=soon)
            elif status == 'not_expired':
                q_filter |= Q(expiration_date__isnull=True) | Q(expiration_date__gt=soon)

        return queryset.filter(q_filter)
