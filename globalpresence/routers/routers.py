from rest_framework.routers import DefaultRouter
from ..viewsets.globalpresence_viewsets import globalpresenceViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('globalpresence', globalpresenceViewsets, basename="globalpresenceViewsets")
