import django_filters
from ..models import NotificationPerUser

class NotificationFilter(django_filters.FilterSet):
    module_name = django_filters.CharFilter(
        field_name="module_name", lookup_expr="iexact"
    )
    # you can also add `icontains` if you want partial search:
    # module_name = django_filters.CharFilter(field_name="module_name", lookup_expr="icontains")

    class Meta:
        model = NotificationPerUser
        fields = ['module_name']