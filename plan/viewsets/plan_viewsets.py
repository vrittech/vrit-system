from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Plan
from ..serializers.plan_serializers import PlanListSerializers, PlanRetrieveSerializers, PlanWriteSerializers
from ..utilities.importbase import *
from rest_framework.decorators import action


class planViewsets(viewsets.ModelViewSet):
    serializer_class = PlanListSerializers
    # permission_classes = [planPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Plan.objects.all().order_by('-order')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','title']
    ordering_fields = ['id','title']

    filterset_fields = {
        'id': ['exact'],
        'is_show': ['exact'],
        'is_popular': ['exact'],
        'created_at': ['exact','gte','lte'],
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

  