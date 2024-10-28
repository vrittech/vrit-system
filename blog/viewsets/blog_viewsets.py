from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Blog
from ..serializers.blog_serializers import BlogListSerializers, BlogRetrieveSerializers, BlogWriteSerializers
from ..utilities.importbase import *
from rest_framework.response import Response
from blog.utilities.permissions import blogPermission

class blogViewsets(viewsets.ModelViewSet):
    serializer_class = BlogListSerializers
    # permission_classes = [blogPermission]
    pagination_class = MyPageNumberPagination
    queryset = Blog.objects.all()

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['title','description','site_title','excerpt','meta_keywords','tags__tag_names']
    ordering_fields = ['id','title', 'description', 'site_title', 'excerpt', 'status','tags__tag_names']
    # ('title', 'description', 'site_title', 'excerpt', 'status', ',('published','Published'),('scheduled','Scheduled')),max_length', 'meta_description', 'meta_keywords', 'meta_author', 'tags', )

    filterset_fields = {
        'title':['exact'],
        'status':['exact'],
        'publish_date':['exact','gte','lte']
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
        #return queryset.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BlogWriteSerializers
        elif self.action == 'retrieve':
            return BlogRetrieveSerializers
        return super().get_serializer_class()
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

