from rest_framework.routers import DefaultRouter
from ..viewsets.gallery_viewsets import galleryViewsets, positionViewsets

router = DefaultRouter()

router.register('custom-gallery', galleryViewsets, basename="galleryViewsets")
router.register('custom-gallery-position', positionViewsets, basename="positionViewsets")
