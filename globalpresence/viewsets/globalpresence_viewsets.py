from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import GlobalPresence
from ..serializers.globalpresence_serializers import GlobalPresenceListSerializers, GlobalPresenceRetrieveSerializers, GlobalPresenceWriteSerializers
from ..utilities.importbase import *
from ..utilities.filters import GlobalPresenceFilter

class globalpresenceViewsets(viewsets.ModelViewSet):
    serializer_class = GlobalPresenceListSerializers
    # permission_classes = [globalpresencePermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = GlobalPresence.objects.all().order_by('created_at')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['global_presence', 'company_name', 'company_address', 'email_address', 'phone_number','id']
    ordering_fields = ['global_presence', 'company_name', 'company_address', 'email_address', 'phone_number','id']
    # ('global_presence', 'company_name', 'company_address', 'email_address', 'phone_number', 'image', )
    filterset_class = GlobalPresenceFilter

    # filterset_fields = {
    #     'id': ['exact'],
    # }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
        #return queryset.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return GlobalPresenceWriteSerializers
        elif self.action == 'retrieve':
            return GlobalPresenceRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

