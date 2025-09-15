from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# 
from ..models import Blog, BlogCategory
from ..serializers.blogs_serializers import BlogCategoryListSerializers, BlogCategoryRetrieveSerializers, BlogCategoryWriteSerializers, BlogsListSerializers, BlogsRetrieveSerializers, BlogsWriteSerializers
from ..utilities.importbase import *
from rest_framework.decorators import action
from rest_framework.response import Response

class blogViewsets(viewsets.ModelViewSet):
    serializer_class = BlogsListSerializers
    # permission_classes = [faqsPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Blog.objects.all().order_by('-order')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    # search_fields = ['question']
    # ordering_fields = ['question']
    def get_object(self):
        lookup_value = self.kwargs.get(self.lookup_field)
        if str(lookup_value).isdigit():
            return get_object_or_404(Blog, pk=lookup_value)
        return get_object_or_404(Blog, slug=lookup_value)
    # ('title', 'description', 'position', 'created_at', 'updated_at', )
    # filterset_class = FaqsFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
        #return queryset.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BlogsWriteSerializers
        elif self.action == 'retrieve':
            return BlogsRetrieveSerializers
        return super().get_serializer_class()


   
class blogsCategoryViewsets(viewsets.ModelViewSet):
    serializer_class = BlogCategoryListSerializers
    # permission_classes = [faqsPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = BlogCategory.objects.all().order_by('-id')

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
            return BlogCategoryWriteSerializers
        elif self.action == 'retrieve':
            return BlogCategoryRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)
    
   