from django.contrib.auth.models import Group, Permission
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from ..serializers.permission_serializers import PermissionSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Permission.objects.all().order_by('-id')
    serializer_class = PermissionSerializer
    permission_classes = [IsAdminUser]
    
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['codename','id','name']
# ('email', 'phone_number', 'position', 'created_at', 'updated_at', )
    filterset_fields = {
        'id':['exact'],
        'name': ['exact','icontains'],
        'codename':['exact','icontains']
    }

