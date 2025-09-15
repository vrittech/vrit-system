from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Testimonial
from ..serializers.testimonial_serializers import TestimonialListSerializers, TestimonialRetrieveSerializers, TestimonialWriteSerializers
from ..utilities.importbase import *
from rest_framework.decorators import action
from django.db.models import Count
from rest_framework.response import Response

class testimonialViewsets(viewsets.ModelViewSet):
    serializer_class = TestimonialListSerializers
    # permission_classes = [testimonialPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Testimonial.objects.all().order_by('-order')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['full_name', 'position', ]
    ordering_fields = ['id','full_name','created_at','description']

    # filterset_fields = {
    #     'id': ['exact'],
    #     'full_name': ['exact'],
    #     'created_at': ['exact','gte','lte'],
    # }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
        #return queryset.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TestimonialWriteSerializers
        elif self.action == 'retrieve':
            return TestimonialRetrieveSerializers
        return super().get_serializer_class()

   