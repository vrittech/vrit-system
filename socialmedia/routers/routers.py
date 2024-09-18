from rest_framework.routers import DefaultRouter
from ..viewsets.socialmedia_viewsets import socialmediaViewsets
from ..viewsets.sitesocialmedia_viewsets import sitesocialmediaViewsets
from ..viewsets.staffhavesocialmedia_viewsets import staffhavesocialmediaViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('socialmedia', socialmediaViewsets, basename="socialmediaViewsets")
router.register('staff-have-socialmedia', staffhavesocialmediaViewsets, basename="staffhavesocialmediaViewsets")
router.register('sitesocialmedia', sitesocialmediaViewsets, basename="sitesocialmediaViewsets")
