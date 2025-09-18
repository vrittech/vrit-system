from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from customgallery.utilities.filters import CustomGalleryFilter
from ..models import CustomGallery as Gallery
from ..serializers.gallery_serializers import GalleryListSerializers, GalleryRetrieveSerializers, GalleryWriteSerializers
from ..utilities.importbase import *
from rest_framework.permissions import DjangoModelPermissions

class galleryViewsets(viewsets.ModelViewSet):
    serializer_class = GalleryListSerializers
    # permission_classes = [DjangoModelPermissions]
    # permission_classes = [galleryPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Gallery.objects.all().distinct().order_by('-id')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['image']
    ordering_fields = ['id']

    filterset_class = CustomGalleryFilter  

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return GalleryWriteSerializers
        elif self.action == 'retrieve':
            return GalleryRetrieveSerializers
        return super().get_serializer_class()



# class positionViewsets(viewsets.ModelViewSet):
#     serializer_class = PositionListSerializers
#     # permission_classes = [DjangoModelPermissions]
#     # permission_classes = [galleryPermission]
#     # authentication_classes = [JWTAuthentication]
#     pagination_class = MyPageNumberPagination
#     queryset = Position.objects.all().distinct().order_by('-id')

#     filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
#     search_fields = ['type','position']
#     ordering_fields = ['type','position']

#     filterset_fields = {
#         'id': ['exact'],  
#         'type':['exact']      
#     }

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         return queryset

#     def get_serializer_class(self):
#         if self.action in ['create', 'update', 'partial_update']:
#             return PositionWriteSerializers
#         elif self.action == 'retrieve':
#             return PositionRetrieveSerializers
#         return super().get_serializer_class()


# class CustomGalleryCategoryViewsets(viewsets.ModelViewSet):
#     serializer_class = CustomGalleryCategoryListSerializers
#     # permission_classes = [faqsPermission]
#     # authentication_classes = [JWTAuthentication]
#     pagination_class = MyPageNumberPagination
#     queryset = CustomGalleryCategory.objects.all().distinct().order_by('-order')

#     filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
#     search_fields = ['name']
#     ordering_fields = ['name']
#     filterset_fields = {
#         'id': ['exact'],
#     }

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         return queryset

#     def get_serializer_class(self):
#         if self.action in ['create', 'update', 'partial_update']:
#             return CustomGalleryCategoryWriteSerializers
#         elif self.action == 'retrieve':
#             return CustomGalleryCategoryRetrieveSerializers
#         return super().get_serializer_class()