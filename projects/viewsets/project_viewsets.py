from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Project,ProjectService
from ..serializers.project_serializers import ProjectListSerializers, ProjectRetrieveSerializers, ProjectWriteSerializers
from ..utilities.importbase import *
from rest_framework.decorators import action
from django.db.models import Count
from rest_framework.response import Response

class projectViewsets(viewsets.ModelViewSet):
    serializer_class = ProjectListSerializers
    # permission_classes = [projectsPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Project.objects.all()

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['name','description']
    ordering_fields = ['id']

    filterset_fields = {
        'id': ['exact'],
        'group': ['exact'],
        'project_service': ['exact'],
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
        #return queryset.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProjectWriteSerializers
        elif self.action == 'retrieve':
            return ProjectRetrieveSerializers
        return super().get_serializer_class()

    @action(detail=False, methods=['get'], name="count_as_services", url_path="services-count")
    def count_as_services(self, request, *args, **kwargs):
        # Group by project_service name and count the number of projects
        service_counts = (
            Project.objects
            .values('project_service__id','project_service__name')  # Group by the service name
            .annotate(project_count=Count('id'))  # Count the number of projects per service
        )

        # Format the response data
        response_data = [
            {
                'service_id': service['project_service__id'],
                'service_name': service['project_service__name'],  # Include service name
                'project_count': service['project_count']
            }
            for service in service_counts
        ]

        return Response(response_data)
    
    @action(detail=False, methods=['get'], name="count_as_group", url_path="project-count")
    def count_as_group(self, request, *args, **kwargs):
        # Group by project_service name and count the number of projects
        groups_counts = (
            Project.objects
            .values('group__id','group__name')  # Group by the service name
            .annotate(project_count=Count('id'))  # Count the number of projects per service
        )

        # Format the response data
        response_data = [
            {
                'service_id': service['group__id'],
                'service_name': service['group__name'],  # Include service name
                'project_count': service['project_count']
            }
            for service in groups_counts
        ]

        return Response(response_data)
