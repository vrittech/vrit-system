from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from faqs.utilities.filter import FaqsFilter
from ..models import Faqs, FaqsCategory
from ..serializers.faqs_serializers import FaqsCategoryListSerializers, FaqsCategoryRetrieveSerializers, FaqsCategoryWriteSerializers, FaqsListSerializers, FaqsRetrieveSerializers, FaqsWriteSerializers
from ..utilities.importbase import *
from rest_framework.decorators import action
from rest_framework.response import Response

class faqsViewsets(viewsets.ModelViewSet):
    serializer_class = FaqsListSerializers
    # permission_classes = [faqsPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Faqs.objects.all().order_by('-order').distinct()

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['question']
    ordering_fields = ['question']
    # ('title', 'description', 'position', 'created_at', 'updated_at', )
    filterset_class = FaqsFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
        #return queryset.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return FaqsWriteSerializers
        elif self.action == 'retrieve':
            return FaqsRetrieveSerializers
        return super().get_serializer_class()


   
class faqsCategoryViewsets(viewsets.ModelViewSet):
    serializer_class = FaqsCategoryListSerializers
    # permission_classes = [faqsPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = FaqsCategory.objects.all().order_by('-order')

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
            return FaqsCategoryWriteSerializers
        elif self.action == 'retrieve':
            return FaqsCategoryRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)
    
   