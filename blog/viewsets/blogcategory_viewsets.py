from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import BlogCategory
from ..serializers.blogcategory_serializers import BlogCategoryListSerializers, BlogCategoryRetrieveSerializers, BlogCategoryWriteSerializers
from ..utilities.importbase import *
from blog.utilities.permissions import blogCategoryPermission

class blogcategoryViewsets(viewsets.ModelViewSet):
    serializer_class = BlogCategoryListSerializers
    # permission_classes = [blogCategoryPermission]
    # authentication_classes = [JWTAuthentication]
    #pagination_class = MyPageNumberPagination
    queryset = BlogCategory.objects.all()

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']

    # filterset_fields = {
    #     'id': ['exact'],
    # }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
        #return queryset.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BlogCategoryWriteSerializers
        elif self.action == 'retrieve':
            return BlogCategoryRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

