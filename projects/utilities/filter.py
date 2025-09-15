from django_filters import rest_framework as filters
from ..models import Project

class ProjectFilter(filters.FilterSet):
    group = filters.BaseInFilter(field_name="group", lookup_expr="in")

    class Meta:
        model = Project
        fields = {
            'id': ['exact'],
            'project_service': ['exact'],
            'created_at': ['exact', 'gte', 'lte']
        }