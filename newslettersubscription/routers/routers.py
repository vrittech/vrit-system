from rest_framework.routers import DefaultRouter
from ..viewsets.newslettersubscription_viewsets import newslettersubscriptionViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('newslettersubscription', newslettersubscriptionViewsets, basename="newslettersubscriptionViewsets")
