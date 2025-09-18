from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from blogs.utilities.filter import BlogFilter

# 
from ..models import Blog, BlogCategory
from ..serializers.blogs_serializers import BlogCategoryListSerializers, BlogCategoryRetrieveSerializers, BlogCategoryWriteSerializers, BlogsListSerializers, BlogsRetrieveSerializers, BlogsWriteSerializers
from ..utilities.importbase import *
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from rest_framework import status

class blogViewsets(viewsets.ModelViewSet):
    serializer_class = BlogsListSerializers
    # permission_classes = [faqsPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Blog.objects.all().distinct().order_by('-order')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['title','user__first_name']
    # ordering_fields = ['question']
    def get_object(self):
        lookup_value = self.kwargs.get(self.lookup_field)
        if str(lookup_value).isdigit():
            return get_object_or_404(Blog, pk=lookup_value)
        return get_object_or_404(Blog, slug=lookup_value)
    # ('title', 'description', 'position', 'created_at', 'updated_at', )
    filterset_class = BlogFilter

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
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

  
    # ------------------------
    # Helpers
    # ------------------------
    def _get_section_queryset(self, request):
        """
        Return queryset for section counts,
        ignoring 'status' filter but applying all others.
        """
        params = request.query_params.copy()
        params.pop("status", None)

        # Temporarily patch request.GET
        original_get = request._request.GET
        request._request.GET = params
        try:
            return self.filter_queryset(self.get_queryset())
        finally:
            request._request.GET = original_get

    def _get_status_counts(self, queryset):
        """
        Return dictionary with counts for each status,
        ensuring all statuses exist with at least 0.
        """
        status_counts = (
            queryset.values("status")
            .annotate(count=Count("status"))
            .order_by()
        )

        counts = {item["status"]: item["count"] for item in status_counts}
        for s in ["draft", "published", "scheduled", "deleted"]:
            counts.setdefault(s, 0)
        return counts

    # ------------------------
    # Main List Method
    # ------------------------
    def list(self, request, *args, **kwargs):
        # Get paginated response (normal filtering, includes status)
        response = super().list(request, *args, **kwargs)

        # Build section queryset (ignoring status filter)
        section_queryset = self._get_section_queryset(request)

        # Build counts
        sections = self._get_status_counts(section_queryset)

        # Inject into response
        response.data["sections"] = sections
        return response



   

    @action(detail=False, methods=['post'], url_path='bulk-delete')
    def bulk_delete(self, request):
        """
        Custom action to soft-delete multiple blogs
        Input: {"delete_ids": [1, 2, 3]}
        """
        delete_ids = request.data.get("delete_ids", [])

        if not delete_ids or not isinstance(delete_ids, list):
            return Response(
                {"error": "Provide delete_ids as a list of blog IDs."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Bulk update
        updated_count = Blog.objects.filter(id__in=delete_ids).update(status="deleted")

        return Response(
            {"message": f"{updated_count} blogs moved to DELETED section."},
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['post'], url_path='bulk-restore')
    def bulk_restore(self, request):
        restore_ids = request.data.get("restore_ids", [])
        if not restore_ids or not isinstance(restore_ids, list):
            return Response(
                {"error": "Provide restore_ids as a list of blog IDs."},
                status=status.HTTP_400_BAD_REQUEST
            )

        updated_count = Blog.objects.filter(id__in=restore_ids).update(status="draft")
        return Response(
            {"message": f"{updated_count} blogs restored to draft."},
            status=status.HTTP_200_OK
        )


   
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
    
   