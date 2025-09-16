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
    search_fields = ['title']
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

    # def list(self, request, *args, **kwargs):
    #     # Always get filtered queryset for the results
    #     queryset = self.filter_queryset(self.get_queryset())

    #     # Pagination logic
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         data = serializer.data
    #     else:
    #         serializer = self.get_serializer(queryset, many=True)
    #         data = serializer.data

    #     # ✅ Decide which queryset to use for sections
    #     if "search" or "category" in request.query_params:
    #         # If ?search is present → sections based on filtered queryset
    #         section_queryset = queryset
    #     else:
    #         # Otherwise → sections based on global queryset (ignore filters)
    #         section_queryset = self.get_queryset()

    #     # Build sections counts
    #     sections = section_queryset.values('status').annotate(count=Count('id'))

    #     # Ensure all statuses are present (with 0 if missing)
    #     all_statuses = dict(Blog._meta.get_field('status').choices)
    #     sections_dict = {status: 0 for status in all_statuses.keys()}
    #     for item in sections:
    #         sections_dict[item['status']] = item['count']

    #     response_data = {
    #         "sections": sections_dict,
    #         "results": data
    #     }
    #     return self.get_paginated_response(response_data) if page is not None else Response(response_data)

    def get_section_queryset(self, request):
        """
        Build queryset for sections:
        - Always respect filters like category, search
        - Ignore status filter
        """
        base_queryset = self.get_queryset()
        params = request.query_params.copy()

        # Remove status filter if present
        params.pop("status", None)

        # Temporarily override request.GET for filtering
        original_params = request.query_params
        request._request.GET = params
        filtered_queryset = self.filter_queryset(base_queryset)
        request._request.GET = original_params  # restore

        return filtered_queryset

    def get_sections(self):
        """
        Return sections counts:
        - Apply all filters except 'status'
        - Always global (ignore pagination)
        """
        base_queryset = self.get_queryset()

        # Apply filters except 'status'
        filters = self.request.query_params.copy()
        filters.pop("status", None)

        # Use your FilterSet manually
        filterset = self.filterset_class(filters, queryset=base_queryset)
        filtered_qs = filterset.qs

        # Aggregate counts
        sections = filtered_qs.values("status").annotate(count=Count("id"))
        all_statuses = dict(Blog._meta.get_field("status").choices)
        sections_dict = {status: 0 for status in all_statuses.keys()}
        for item in sections:
            sections_dict[item["status"]] = item["count"]
        return sections_dict

    # --------------------------
    # List override
    # --------------------------

    def list(self, request, *args, **kwargs):
        # Full filtered queryset (all filters applied)
        queryset = self.filter_queryset(self.get_queryset())

        # Paginate results
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page if page is not None else queryset, many=True)
        results = serializer.data

        # Build global section counts
        sections_dict = self.get_sections()

        # Build response
        if page is not None:
            paginated_response = self.get_paginated_response(results)
            response_data = paginated_response.data
        else:
            response_data = {
                "count": len(results),
                "next": None,
                "previous": None,
                "results": results,
            }

        # Inject sections at the top level
        response_data["sections"] = sections_dict

        return Response(response_data)

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
    
   