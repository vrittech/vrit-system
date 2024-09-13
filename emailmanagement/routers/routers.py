from rest_framework.routers import DefaultRouter
from ..viewsets.emailsetup_viewsets import emailsetupViewsets
from ..viewsets.emailmanagement_viewsets import emailmanagementViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('email-setup', emailsetupViewsets, basename="emailsetupViewsets")
router.register('email-management', emailmanagementViewsets, basename="emailmanagementViewsets")
