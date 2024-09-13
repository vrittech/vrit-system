from rest_framework.routers import DefaultRouter
from ..viewsets.emailsetup_viewsets import emailsetupViewsets
from ..viewsets.emailmanagement_viewsets import emailmanagementViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('emailsetup', emailsetupViewsets, basename="emailsetupViewsets")
router.register('emailmanagement', emailmanagementViewsets, basename="emailmanagementViewsets")
