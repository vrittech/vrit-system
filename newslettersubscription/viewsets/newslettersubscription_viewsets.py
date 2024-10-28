from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import NewsLetterSubscription
from ..serializers.newslettersubscription_serializers import NewsLetterSubscriptionListSerializers, NewsLetterSubscriptionRetrieveSerializers, NewsLetterSubscriptionWriteSerializers
from ..utilities.importbase import *

class newslettersubscriptionViewsets(viewsets.ModelViewSet):
    serializer_class = NewsLetterSubscriptionListSerializers
    # permission_classes = [newslettersubscriptionPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = NewsLetterSubscription.objects.all().order_by('created_at')
    # ('name', 'email', 'is_subscribed', 'category', 'date', 'created_at', 'updated_at', )

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['name', 'email', 'is_subscribed', 'category', 'date', 'created_at', 'updated_at','id']
    ordering_fields = ['name', 'email', 'is_subscribed', 'category', 'date', 'created_at', 'updated_at','id']

    filterset_fields = {
        'id': ['exact'],
        'category': ['exact'],
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
        #return queryset.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return NewsLetterSubscriptionWriteSerializers
        elif self.action == 'retrieve':
            return NewsLetterSubscriptionRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

