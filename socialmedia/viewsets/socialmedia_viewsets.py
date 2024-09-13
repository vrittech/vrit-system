from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import SocialMedia
from ..serializers.socialmedia_serializers import SocialMediaListSerializers, SocialMediaRetrieveSerializers, SocialMediaWriteSerializers
from ..utilities.importbase import *

class socialmediaViewsets(viewsets.ModelViewSet):
    serializer_class = SocialMediaListSerializers
    # permission_classes = [socialmediaPermission]
    # authentication_classes = [JWTAuthentication]
    #pagination_class = MyPageNumberPagination
    queryset = SocialMedia.objects.all()

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
            return SocialMediaWriteSerializers
        elif self.action == 'retrieve':
            return SocialMediaRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

