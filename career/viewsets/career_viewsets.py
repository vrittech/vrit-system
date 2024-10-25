from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Career
from ..serializers.career_serializers import CareerListSerializers, CareerRetrieveSerializers, CareerWriteSerializers
from ..utilities.importbase import *
from ..utilities.carrer_filter import CareerFilter

class careerViewsets(viewsets.ModelViewSet):
    serializer_class = CareerListSerializers
    # permission_classes = [careerPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Career.objects.all()
    filterset_class = CareerFilter

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
            return CareerWriteSerializers
        elif self.action == 'retrieve':
            return CareerRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

