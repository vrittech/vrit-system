from rest_framework.routers import DefaultRouter
from ..viewsets.inquires_viewsets import inquiresViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('inquires', inquiresViewsets, basename="inquiresViewsets")
