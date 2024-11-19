from django.apps import apps
from django.contrib.auth.models import Permission
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..serializers.permission_serializers import PermissionSerializer

class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        # Dynamically identify custom apps by excluding built-in and third-party apps
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

        # Get all installed apps and exclude the built-in/third-party ones
        custom_app_labels = [
            app.label for app in apps.get_app_configs()
            if app.name not in excluded_apps
        ]

        # Fetch permissions related to these custom apps
        return Permission.objects.filter(
            content_type__app_label__in=custom_app_labels
        ).order_by('-id')

    serializer_class = PermissionSerializer
    permission_classes = [IsAdminUser]
    
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['codename', 'id', 'name']
    filterset_fields = {
        'id': ['exact'],
        'name': ['exact', 'icontains'],
        'codename': ['exact', 'icontains']
    }
