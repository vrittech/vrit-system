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
from rest_framework.decorators import action
from rest_framework import status
from django.db.models import Count
from rest_framework.response import Response

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

    @action(detail=False, methods=['get'], url_path='album-image-counts')
    def album_image_counts(self, request, *args, **kwargs):
            """
            Custom action to return the count of images in each album.
            """
            # Calculate image count for each album
            albums_with_image_count = Album.objects.annotate(
                image_count=Count('career_galleries')
            ).values('id', 'title', 'image_count')

            # Prepare the response data
            response_data = {
                'albums': list(albums_with_image_count)
            }

            return Response(response_data, status=status.HTTP_200_OK)
