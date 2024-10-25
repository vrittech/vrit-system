from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from ..models import CareerGallery, Album
from ..serializers.careergallery_serializers import (
    CareerGalleryListSerializers, 
    CareerGalleryRetrieveSerializers, 
    CareerGalleryWriteSerializers
)
from ..utilities.importbase import *

class careergalleryViewsets(viewsets.ModelViewSet):
    serializer_class = CareerGalleryListSerializers
    # permission_classes = [careergalleryPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = CareerGallery.objects.all()

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id','name','created_at','album__title','name']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Annotate queryset with image count for each album
        queryset = queryset.select_related('album').annotate(
            image_count=Count('album__career_galleries')
        )

        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CareerGalleryWriteSerializers
        elif self.action == 'retrieve':
            return CareerGalleryRetrieveSerializers
        return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Aggregating image count for each album
        albums_with_image_count = Album.objects.annotate(
            image_count=Count('career_galleries')
        ).values('id', 'title', 'image_count')

        response_data = {
            "albums": list(albums_with_image_count),
            "career_galleries": self.get_serializer(queryset, many=True).data
        }

        return Response(response_data)
