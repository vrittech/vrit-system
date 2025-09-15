from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from services.utilities.filter import ServicesFilter
from ..models import Services, ServicesCategory
from ..serializers.services_serializers import ServicesCategoryListSerializers, ServicesCategoryRetrieveSerializers, ServicesCategoryWriteSerializers, ServicesListSerializers, ServicesRetrieveSerializers, ServicesWriteSerializers
from ..utilities.importbase import *
from rest_framework.decorators import action
from django.db.models import Count
from rest_framework.response import Response

class servicesViewsets(viewsets.ModelViewSet):
    serializer_class = ServicesListSerializers
    # permission_classes = [testimonialPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Services.objects.all().distinct().order_by('-order')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','name']
    ordering_fields = ['id','name']
    filterset_class = ServicesFilter

    # filterset_fields = {
    #     'id': ['exact'],
    #     'full_name': ['exact'],
    #     'created_at': ['exact','gte','lte'],
    # }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
        #return queryset.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ServicesWriteSerializers
        elif self.action == 'retrieve':
            return ServicesRetrieveSerializers
        return super().get_serializer_class()
    



class servicesCategoryViewsets(viewsets.ModelViewSet):
    serializer_class = ServicesCategoryListSerializers
    # permission_classes = [testimonialPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = ServicesCategory.objects.all().order_by('-order')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','name']
    ordering_fields = ['id','name']

    # filterset_fields = {
    #     'id': ['exact'],
    #     'full_name': ['exact'],
    #     'created_at': ['exact','gte','lte'],
    # }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
        #return queryset.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ServicesCategoryWriteSerializers
        elif self.action == 'retrieve':
            return ServicesCategoryRetrieveSerializers
        return super().get_serializer_class()

   