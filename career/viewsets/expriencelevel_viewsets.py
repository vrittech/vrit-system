from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import ExprienceLevel
from ..serializers.expriencelevel_serializers import ExprienceLevelListSerializers, ExprienceLevelRetrieveSerializers, ExprienceLevelWriteSerializers
from ..utilities.importbase import *

class expriencelevelViewsets(viewsets.ModelViewSet):
    serializer_class = ExprienceLevelListSerializers
    # permission_classes = [careerPermission]
    # authentication_classes = [JWTAuthentication]
    #pagination_class = MyPageNumberPagination
    queryset = ExprienceLevel.objects.all()

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']

    # filterset_fields = {
    #     'id': ['exact'],
    # }

    def get_queryset(self):
        queryset = super().get_queryset()
        #return queryset.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ExprienceLevelWriteSerializers
        elif self.action == 'retrieve':
            return ExprienceLevelRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

