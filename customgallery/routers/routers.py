from rest_framework.routers import DefaultRouter
from ..viewsets.gallery_viewsets import CustomGalleryCategoryViewsets, galleryViewsets, positionViewsets

router = DefaultRouter()

router.register('custom-gallery', galleryViewsets, basename="galleryViewsets")
router.register('custom-gallery-position', positionViewsets, basename="positionViewsets")
router.register('custom-gallery-category', CustomGalleryCategoryViewsets, basename="CustomGalleryCategoryViewsets")
