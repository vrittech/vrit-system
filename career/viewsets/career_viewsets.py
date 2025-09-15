from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Career
from ..serializers.career_serializers import CareerListSerializers, CareerRetrieveSerializers, CareerWriteSerializers
from ..utilities.importbase import *
from ..utilities.carrer_filter import CareerFilter
from rest_framework.response import Response
from rest_framework.decorators import action

class careerViewsets(viewsets.ModelViewSet):
    serializer_class = CareerListSerializers
    # permission_classes = [careerPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Career.objects.all().order_by('-order').distinct()
    filterset_class = CareerFilter

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','title']
    ordering_fields = ['id','title']
    # ('title', 'experience_level', 'description', 'position', 'num_of_vacancy', 'apply_link', 'image', 'is_show', 'enable_auto_expiration', 'expiration_date', 'created_at', 'updated_at', )
    
    # filterset_class = CareerFilter
    def get_object(self):
        lookup_value = self.kwargs.get(self.lookup_field)
        if str(lookup_value).isdigit():
            return get_object_or_404(Career, pk=lookup_value)
        return get_object_or_404(Career, slug=lookup_value)

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
