from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import EmailManagement
from ..serializers.emailmanagement_serializers import EmailManagementListSerializers, EmailManagementRetrieveSerializers, EmailManagementWriteSerializers
from ..utilities.importbase import *

class emailmanagementViewsets(viewsets.ModelViewSet):
    serializer_class = EmailManagementListSerializers
    # permission_classes = [emailmanagementPermission]
    # authentication_classes = [JWTAuthentication]
    #pagination_class = MyPageNumberPagination
    queryset = EmailManagement.objects.all()

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']

    # filterset_fields = {
    #     'id': ['exact'],
    # }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
        #return queryset.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return EmailManagementWriteSerializers
        elif self.action == 'retrieve':
            return EmailManagementRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

