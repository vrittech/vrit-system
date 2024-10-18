from rest_framework.routers import DefaultRouter
from ..viewsets.album_viewsets import albumViewsets
from ..viewsets.careergallery_viewsets import careergalleryViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('album', albumViewsets, basename="albumViewsets")
router.register('careergallery', careergalleryViewsets, basename="careergalleryViewsets")
