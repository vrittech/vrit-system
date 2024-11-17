from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import ContactUs
from ..serializers.contactus_serializers import ContactUsListSerializers, ContactUsRetrieveSerializers, ContactUsWriteSerializers
from ..utilities.importbase import *

class contactusViewsets(viewsets.ModelViewSet):
    serializer_class = ContactUsListSerializers
    # permission_classes = [faqsPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = ContactUs.objects.all().order_by('-position')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','email', 'phone_number', 'position', 'created_at', 'updated_at',]
    ordering_fields = ['id','email', 'phone_number', 'position', 'created_at', 'updated_at',]
# ('email', 'phone_number', 'position', 'created_at', 'updated_at', )
    filterset_fields = {
        'created_at': ['exact','gte','lte'],
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ContactUsWriteSerializers
        elif self.action == 'retrieve':
            return ContactUsRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

