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

class clientsViewsets(viewsets.ModelViewSet):
    serializer_class = ClientsListSerializers
    # permission_classes = [clientsPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Clients.objects.all().order_by('created_at')

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
        
        # Calculate section-wise counts
        section_counts = (
            queryset
            .values('section')
            .annotate(count=Count('section'))
            .order_by('section')
        )
        
        # Calculate total count of all clients
        total_count = queryset.count()

        # Combine the results
        response_data = {
            'section_counts': section_counts,
            'total_count': total_count
        }

        return Response(response_data, status=status.HTTP_200_OK)

