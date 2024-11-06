from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Career
from ..serializers.career_serializers import CareerListSerializers, CareerRetrieveSerializers, CareerWriteSerializers
from ..utilities.importbase import *
from ..utilities.carrer_filter import CareerFilter
from rest_framework.response import Response
from rest_framework.decorators import action

class careerViewsets(viewsets.ModelViewSet):
    serializer_class = CareerListSerializers
    # permission_classes = [careerPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Career.objects.all().order_by('position')
    filterset_class = CareerFilter

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','title', 'experience_level', 'description', 'position', 'num_of_vacancy', 'apply_link', 'image', 'is_show', 'enable_auto_expiration', 'expiration_date', 'created_at', 'updated_at',]
    ordering_fields = ['id','title','expiration_date','created_at']
    # ('title', 'experience_level', 'description', 'position', 'num_of_vacancy', 'apply_link', 'image', 'is_show', 'enable_auto_expiration', 'expiration_date', 'created_at', 'updated_at', )
    
    # filterset_class = CareerFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
        #return queryset.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CareerWriteSerializers
        elif self.action == 'retrieve':
            return CareerRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'], name="draggableClient", url_path="drag-client")
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
            target_obj = Career.objects.get(position=target_position)
            goal_obj = Career.objects.get(position=goal_position)
        except Career.DoesNotExist:
            return Response({"error": "Target or Goal object not found"}, status=400)

        if target_position < goal_position:
            # Moving target down (target goes after goal)
            affected_objs = Career.objects.filter(
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
            affected_objs = Career.objects.filter(
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

