from rest_framework.routers import DefaultRouter
from ..viewsets.services_viewsets import servicesCategoryViewsets, servicesViewsets

router = DefaultRouter()


router.register('services', servicesViewsets, basename="servicesViewsets")
router.register('services-category', servicesCategoryViewsets, basename="servicesCategoryViewsets")
