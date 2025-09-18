from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from web_branding.models import Position, WebBranding, WebBrandingCategory
from web_branding.serializers.web_branding_serializers import PositionListSerializers, PositionRetrieveSerializers, PositionWriteSerializers, WebBrandingCategoryListSerializers, WebBrandingCategoryRetrieveSerializers, WebBrandingCategoryWriteSerializers, WebBrandingListSerializers, WebBrandingRetrieveSerializers, WebBrandingWriteSerializers
from web_branding.utilities.filters import WebBrandingFilter
from ..utilities.importbase import *
from rest_framework.permissions import DjangoModelPermissions

class webBrandingViewsets(viewsets.ModelViewSet):
    serializer_class = WebBrandingListSerializers
    # permission_classes = [DjangoModelPermissions]
    # permission_classes = [galleryPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = WebBranding.objects.all().distinct().order_by('-id')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['image']
    ordering_fields = ['id']

    filterset_class = WebBrandingFilter  

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return WebBrandingWriteSerializers
        elif self.action == 'retrieve':
            return WebBrandingRetrieveSerializers
        return super().get_serializer_class()



class positionViewsets(viewsets.ModelViewSet):
    serializer_class = PositionListSerializers
    # permission_classes = [DjangoModelPermissions]
    # permission_classes = [galleryPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Position.objects.all().distinct().order_by('-id')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['type','position']
    ordering_fields = ['type','position']

    filterset_fields = {
        'id': ['exact'],  
        'type':['exact']      
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PositionWriteSerializers
        elif self.action == 'retrieve':
            return PositionRetrieveSerializers
        return super().get_serializer_class()


class WebBrandingCategoryViewsets(viewsets.ModelViewSet):
    serializer_class = WebBrandingCategoryListSerializers
    # permission_classes = [faqsPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = WebBrandingCategory.objects.all().distinct().order_by('-order')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    filterset_fields = {
        'id': ['exact'],
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return WebBrandingCategoryWriteSerializers
        elif self.action == 'retrieve':
            return WebBrandingCategoryRetrieveSerializers
        return super().get_serializer_class()