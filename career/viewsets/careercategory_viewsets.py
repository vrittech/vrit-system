from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from career.serializers.careercategory_serializers import CareerCategoryListSerializers, CareerCategoryRetrieveSerializers, CareerCategoryWriteSerializers
from ..models import CareerCategory, ExperienceLevel
from ..serializers.expriencelevel_serializers import ExperienceLevelListSerializers, ExperienceLevelRetrieveSerializers, ExperienceLevelWriteSerializers
from ..utilities.importbase import *

class careerCategoryViewsets(viewsets.ModelViewSet):
    serializer_class = CareerCategoryListSerializers
    # permission_classes = [careerPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = CareerCategory.objects.all().order_by('-order')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
        #return queryset.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CareerCategoryWriteSerializers
        elif self.action == 'retrieve':
            return CareerCategoryRetrieveSerializers
        return super().get_serializer_class()

    
    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

