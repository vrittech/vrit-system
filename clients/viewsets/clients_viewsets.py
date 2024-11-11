from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Clients
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import action
from ..serializers.clients_serializers import ClientsListSerializers, ClientsRetrieveSerializers, ClientsWriteSerializers
from ..utilities.importbase import *
from django.db.models import Count
from collections import defaultdict

SECTION_CHOICES = [
    ('first', 'First'),
    ('second', 'Second'),
    ('third', 'Third'),
    ('fourth', 'Fourth'),
]

class clientsViewsets(viewsets.ModelViewSet):
    serializer_class = ClientsListSerializers
    # permission_classes = [clientsPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Clients.objects.all().order_by('position')
    lookup_field = "slug"

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','name', 'section', 'created_at', 'updated_at',]
    ordering_fields = ['id','name', 'section', 'created_at', 'updated_at',]
    # ('SECTION_CHOICES', 'LOOP_TYPE_CHOICES', 'client', 'section', 'loop_type', 'delay_time', 'created_at', 'updated_at', )
# ('name', 'section', )
    filterset_fields = {
        'id': ['exact'],
        'name': ['exact'],
        'section': ['exact'],
        'created_at': ['exact','gte','lte'],
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
        #return queryset.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ClientsWriteSerializers
        elif self.action == 'retrieve':
            return ClientsRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)
    @action(detail=False, methods=['get'], url_path='section-counts')
    def section_counts(self, request, *args, **kwargs):
        """
        Custom action to return the count of clients in each section
        along with the total count of all clients.
        """
        queryset = self.get_queryset()
    
        # Calculate section-wise counts from the database
        section_counts_query = (
            queryset
            .values('section')
            .annotate(count=Count('section'))
            .order_by('section')
        )

        # Convert section counts query to a dictionary with default count 0
        section_counts_dict = defaultdict(int, {item['section']: item['count'] for item in section_counts_query})
        
        # Prepare the response including all sections with counts, defaulting to 0 where necessary
        section_counts = [
            {'section': section_key, 'count': section_counts_dict.get(section_key, 0)}
            for section_key, _ in SECTION_CHOICES
        ]

        # Calculate total count of all clients
        total_count = queryset.count()

        # Combine the results
        response_data = {
            'section_counts': section_counts,
            'all': total_count
        }

        return Response(response_data, status=status.HTTP_200_OK)

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
            target_obj = Clients.objects.get(position=target_position)
            goal_obj = Clients.objects.get(position=goal_position)
        except Clients.DoesNotExist:
            return Response({"error": "Target or Goal object not found"}, status=400)

        if target_position < goal_position:
            # Moving target down (target goes after goal)
            affected_objs = Clients.objects.filter(
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
            affected_objs = Clients.objects.filter(
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

