from rest_framework.routers import DefaultRouter
from ..viewsets.globalpresence_viewsets import globalpresenceViewsets
from ..viewsets.country_viewsets import countryViewsets

router = DefaultRouter()


router.register('global-presence', globalpresenceViewsets, basename="globalpresenceViewsets")
router.register('country', countryViewsets, basename="countryViewsets")
