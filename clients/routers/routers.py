from rest_framework.routers import DefaultRouter
from ..viewsets.clients_viewsets import clientsViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('clients', clientsViewsets, basename="clientsViewsets")
