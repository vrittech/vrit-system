# gallery/filters.py
import django_filters
from ..models import CustomGallery
from django.db.models import Q

class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass

class CustomGalleryFilter(django_filters.FilterSet):
    # match ?is_static=true or ?is_static=false
    # is_static = django_filters.BooleanFilter(field_name="is_static")

    # match ?position=homepage (this goes through FK to Position.type)
    # page_type = django_filters.CharFilter(field_name="position__type", lookup_expr="exact")

    # category = NumberInFilter(field_name="category", lookup_expr="in", method="filter_category")

    class Meta:
        model = CustomGallery
        fields = ['id']

    # def filter_category(self, queryset, name, value):
    #     """
    #     If -1 is passed, return FAQs with no category.
    #     Otherwise, filter by the given list of category IDs.
    #     """
    #     if value and "-1" in [str(v) for v in value]:
    #         return queryset.filter(Q(category__isnull=True))
    #     return queryset.filter(**{f"{name}__in": value})
