from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Forms
from ..serializers.forms_serializers import FormsListSerializers, FormsRetrieveSerializers, FormsWriteSerializers
from ..utilities.importbase import *
from django.db.models import Count, Value
from django.db.models.functions import Coalesce
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from ..models import Forms, Category

class formsViewsets(viewsets.ModelViewSet):
    serializer_class = FormsListSerializers
    # permission_classes = [formsPermission]
    # authentication_classes = [JWTAuthentication]
    #pagination_class = MyPageNumberPagination
    queryset = Forms.objects.all()

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','title', 'category', 'description', 'header_code', 'embedded_code', 'image', 'excerpt', 'auto_expiration', 'is_expired', 'auto_expiration_date', 'position',]
    ordering_fields = ['id','title', 'category', 'description', 'header_code', 'embedded_code','excerpt', 'auto_expiration', 'is_expired', 'auto_expiration_date', 'position',]
    # ('title', 'category', 'description', 'header_code', 'embedded_code', 'image', 'excerpt', 'auto_expiration', 'is_expired', 'auto_expiration_date', 'position', )

    filterset_fields = {
        'id': ['exact'],
        'auto_expiration_date': ['exact'],
        'is_show': ['exact'],
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        #return queryset.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return FormsWriteSerializers
        elif self.action == 'retrieve':
            return FormsRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'], name="category_form_counts", url_path="category-form-counts")
    def category_form_counts(self, request, *args, **kwargs):
        # Count forms by category, including categories with 0 forms
        category_counts = (
            Category.objects
            .annotate(count=Coalesce(Count('forms'), Value(0)))
            .values('name', 'count')
            .order_by('name')
        )

        # Total count of all forms
        total_count = Forms.objects.count()

        # Format the response
        response_data = {
            "category_counts": category_counts,
            "total_count": total_count
        }

        return Response(response_data)

