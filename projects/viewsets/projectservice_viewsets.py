from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import ProjectService
from ..serializers.projectservice_serializers import ProjectServiceListSerializers, ProjectServiceRetrieveSerializers, ProjectServiceWriteSerializers
from ..utilities.importbase import *
from rest_framework.decorators import action

class projectserviceViewsets(viewsets.ModelViewSet):
    serializer_class = ProjectServiceListSerializers
    # permission_classes = [projectsPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = ProjectService.objects.all().order_by('position')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ('id','name', 'description', 'position', 'is_feature', 'created_at', 'updated_at', )
    ordering_fields = ('id','name', 'description', 'position', 'is_feature', 'created_at', 'updated_at', )
    # ('name', 'description', 'image', 'position', 'is_feature', 'created_at', 'updated_at', )

    filterset_fields = {
        'id': ['exact'],
        'name': ['exact'],
        'position': ['exact'],
        'is_feature': ['exact'],
        'created_at': ['exact','gte','lte'],
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
        #return queryset.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProjectServiceWriteSerializers
        elif self.action == 'retrieve':
            return ProjectServiceRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'], name="draggableProject", url_path="drag-project-service")
    def Draggable(self, request, *args, **kwargs):
        target = request.GET.get('target')  # ID of the target object 
        goal = request.GET.get('goal')  # ID of the goal object 

        from rest_framework.response import Response

        # Fetch the target and goal objects
        try:
            target_obj = ProjectService.objects.get(id=target)
            goal_obj = ProjectService.objects.get(id=goal)
        except ProjectService.DoesNotExist:
            return Response({"error": "Target or Goal object not found"}, status=400)

        target_position = target_obj.position
        goal_position = goal_obj.position

        if target_position < goal_position:
            # Moving target down (target goes after goal)
            affected_objs = ProjectService.objects.filter(position__gt=target_position, position__lte=goal_position).order_by('position')
            
            # Decrement position of all affected objects
            for obj in affected_objs:
                obj.position -= 1
                obj.save()
            
            # Set target object's new position
            target_obj.position = goal_position
            target_obj.save()

        else:
          # Moving target up (target goes before goal)
            affected_objs = ProjectService.objects.filter(position__lt=target_position, position__gte=goal_position).order_by('-position')

            # Increment position of all affected objects by 1
            for obj in affected_objs:
                obj.position += 1
                obj.save()

            # Set target object's new position (exact position of the goal)
            target_obj.position = goal_position  # Place the target in the goal's position
            target_obj.save()


        return Response({"status": "success"})

