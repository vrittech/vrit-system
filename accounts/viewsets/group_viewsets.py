from django.contrib.auth.models import Group, Permission
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from ..serializers.group_serializers import GroupSerializer
from ..utilities.importbase import *
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('-id')
    serializer_class = GroupSerializer
    pagination_class = MyPageNumberPagination
    # permission_classes = [IsAdminUser]


