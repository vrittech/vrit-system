import django_filters
from django_filters import rest_framework as filters
from ..models import EmailLog

class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass

class EmailLogFilter(filters.FilterSet):
    date = filters.DateFilter(field_name='date')
    time = filters.TimeFilter(field_name='time')
    subject = filters.CharFilter(field_name='subject', lookup_expr='icontains')
    purpose = CharInFilter(field_name='purpose', lookup_expr='in')  # Allows multiple purposes
    recipient = CharInFilter(field_name='recipient', lookup_expr='in')  # Allows multiple recipients
    status = CharInFilter(field_name='status', lookup_expr='in')  # Allows multiple statuses
    created_at = filters.DateFromToRangeFilter(field_name='created_at')

    class Meta:
        model = EmailLog
        fields = ['date', 'time', 'subject', 'purpose', 'recipient', 'status', 'created_at']
