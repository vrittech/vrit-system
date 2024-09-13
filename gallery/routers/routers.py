from rest_framework.routers import DefaultRouter
from ..viewsets.gallery_viewsets import galleryViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('gallery', galleryViewsets, basename="galleryViewsets")
