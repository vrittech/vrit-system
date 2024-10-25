from rest_framework.routers import DefaultRouter
from ..viewsets.clients_viewsets import clientsViewsets
from ..viewsets.clientsettings_viewsets import clientsettingsViewsets

router = DefaultRouter()


router.register('clients', clientsViewsets, basename="clientsViewsets")
router.register('clientsettings', clientsettingsViewsets, basename="clientsettingsViewsets")
