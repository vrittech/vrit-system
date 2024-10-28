from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Plan
from ..serializers.plan_serializers import PlanListSerializers, PlanRetrieveSerializers, PlanWriteSerializers
from ..utilities.importbase import *

class planViewsets(viewsets.ModelViewSet):
    serializer_class = PlanListSerializers
    # permission_classes = [planPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Plan.objects.all().order_by('position')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','title', 'pricing', 'duration', 'description', 'features', 'is_show', 'is_popular', 'position', 'created_at', 'updated_at',]
    ordering_fields = ['id','title', 'pricing', 'duration', 'description', 'features', 'is_show', 'is_popular', 'position', 'created_at', 'updated_at',]
    # ('title', 'pricing', 'duration', 'description', 'features', 'is_show', 'is_popular', 'position', 'created_at', 'updated_at', )

    filterset_fields = {
        'id': ['exact'],
        'is_show': ['exact'],
        'is_popular': ['exact'],
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
        #return queryset.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PlanWriteSerializers
        elif self.action == 'retrieve':
            return PlanRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

