from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Project,ProjectService
from ..serializers.project_serializers import ProjectListSerializers, ProjectRetrieveSerializers, ProjectWriteSerializers
from ..utilities.importbase import *
from rest_framework.decorators import action
from django.db.models import Count
from rest_framework.response import Response
from django.db.models import F

class projectViewsets(viewsets.ModelViewSet):
    # http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    serializer_class = ProjectListSerializers
    # permission_classes = [projectsPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Project.objects.all().order_by("position")

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ('id','name', 'position', 'description', 'group__name', 'project_service__name', 'project_link__label', 'case_study__title', 'created_at', 'updated_at', )
    ordering_fields = ('id','name','created_at', )
    # ('name', 'position', 'description', 'group', 'project_service', 'project_link', 'case_study', 'media', 'created_at', 'updated_at', )

    filterset_fields = {
        'id': ['exact'],
        'group': ['exact'],
        'project_service': ['exact'],
        'created_at':['exact','gte','lte']
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


    @action(detail=False, methods=['get'], name="draggableProject", url_path="drag-project")
    def Draggable(self, request, *args, **kwargs):
        target_position = request.GET.get('target')  # Position of the target object
        goal_position = request.GET.get('goal')  # Position of the goal object

        from rest_framework.response import Response

        if not target_position or not goal_position:
            return Response({"error": "Target or Goal position not provided"}, status=400)

        # Convert to integers
        try:
            target_position = int(target_position)
            goal_position = int(goal_position)
        except ValueError:
            return Response({"error": "Invalid target or goal position"}, status=400)

        # Fetch the target and goal objects based on position
        try:
            target_obj = Project.objects.get(position=target_position)
            goal_obj = Project.objects.get(position=goal_position)
        except Project.DoesNotExist:
            return Response({"error": "Target or Goal object not found"}, status=400)

        if target_position < goal_position:
            # Moving target down (target goes after goal)
            affected_objs = Project.objects.filter(
                position__gt=target_position, position__lte=goal_position
            ).order_by('position')
            
            # Decrement position of all affected objects
            for obj in affected_objs:
                obj.position -= 1
                obj.save()

            # Set target object's new position
            target_obj.position = goal_position
            target_obj.save()

        else:
            # Moving target up (target goes before goal)
            affected_objs = Project.objects.filter(
                position__lt=target_position, position__gte=goal_position
            ).order_by('-position')

            # Increment position of all affected objects by 1
            for obj in affected_objs:
                obj.position += 1
                obj.save()

            # Set target object's new position (exact position of the goal)
            target_obj.position = goal_position
            target_obj.save()

        return Response({"status": "success"})



