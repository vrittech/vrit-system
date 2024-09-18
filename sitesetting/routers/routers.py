from rest_framework.routers import DefaultRouter
from ..viewsets.sitesetting_viewsets import sitesettingViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('sitesetting', sitesettingViewsets, basename="sitesettingViewsets")
