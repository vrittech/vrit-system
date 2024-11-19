from django.apps import apps
from django.contrib.auth.models import Permission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from collections import defaultdict
from ..serializers.permission_serializers import PermissionSerializer


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet to list permissions and provide an additional grouped-by-apps view.
    """
    serializer_class = PermissionSerializer
    permission_classes = [IsAdminUser]

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['codename', 'id', 'name']
    filterset_fields = {
        'id': ['exact'],
        'name': ['exact', 'icontains'],
        'codename': ['exact', 'icontains']
    }

    def get_queryset(self):
        """
        Dynamically fetch permissions for custom apps.
        """
        # Define excluded apps (Django built-in and third-party)
        excluded_apps = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'corsheaders',
            'rest_framework',
            'drf_yasg',
            'django_celery_beat',
            'django_filters',
        ]

        # Dynamically identify custom app labels
        custom_app_labels = [
            app.label for app in apps.get_app_configs()
            if app.name not in excluded_apps
        ]

        # Fetch permissions related to these custom apps
        return Permission.objects.filter(
            content_type__app_label__in=custom_app_labels
        ).select_related('content_type')

    @action(detail=False, methods=['get'])
    def grouped_by_app(self, request):
        """
        Additional action to group permissions by apps.
        """
        # Get queryset (permissions)
        permissions = self.get_queryset()

        # Group permissions by app
        grouped_permissions = defaultdict(list)
        for permission in permissions:
            grouped_permissions[permission.content_type.app_label].append({
                'id': permission.id,
                'name': permission.name,
                'codename': permission.codename,
                'model': permission.content_type.model,
            })

        # Convert grouped data to a regular dict for serialization
        return Response(dict(grouped_permissions))
