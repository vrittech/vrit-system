from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Clients
from ..serializers.clients_serializers import ClientsListSerializers, ClientsRetrieveSerializers, ClientsWriteSerializers
from ..utilities.importbase import *

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

