# gallery/filters.py
import django_filters
from ..models import CustomGallery

class CustomGalleryFilter(django_filters.FilterSet):
    # match ?is_static=true or ?is_static=false
    is_static = django_filters.BooleanFilter(field_name="is_static")

    # match ?position=homepage (this goes through FK to Position.type)
    position = django_filters.CharFilter(field_name="position__type", lookup_expr="exact")

    class Meta:
        model = CustomGallery
        fields = ['is_static', 'position']
