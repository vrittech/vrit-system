from django_filters import rest_framework as filters
from ..models import NewsLetterSubscription

# Custom filter to allow multiple IDs for categories
class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass

class NewsLetterSubscriptionFilter(filters.FilterSet):
    category = NumberInFilter(field_name='category__id', lookup_expr='in')

    class Meta:
        model = NewsLetterSubscription
        fields = ['id', 'category']
