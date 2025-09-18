from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Inquires
from ..serializers.inquires_serializers import InquiresListSerializers, InquiresRetrieveSerializers, InquiresWriteSerializers
from ..utilities.importbase import *
from ..utilities.inquires_filter import InquiresFilter

class inquiresViewsets(viewsets.ModelViewSet):
    serializer_class = InquiresListSerializers
    # permission_classes = [inquiresPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Inquires.objects.all().order_by('created_at').distinct()

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['full_name','phone_number','company_name']
    ordering_fields = ['id','full_name','company_name','created_at']
    # ('project_service', 'project_plan', 'first_name', 'last_name', 'email_address', 'phone_number', 'company_name', 'project_detail', 'created_at', 'updated_at', )
    filterset_class = InquiresFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
        #return queryset.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return InquiresWriteSerializers
        elif self.action == 'retrieve':
            return InquiresRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

