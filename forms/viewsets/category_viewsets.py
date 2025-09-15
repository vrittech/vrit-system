from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Category
from ..serializers.category_serializers import CategoryListSerializers, CategoryRetrieveSerializers, CategoryWriteSerializers
from ..utilities.importbase import *

class categoryViewsets(viewsets.ModelViewSet):
    serializer_class = CategoryListSerializers
    # permission_classes = [formsPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Category.objects.all().order_by('-order')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','name']
    ordering_fields = ['id','order']

    # filterset_fields = {
    #     'id': ['exact'],
    # }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CategoryWriteSerializers
        elif self.action == 'retrieve':
            return CategoryRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

