from rest_framework.routers import DefaultRouter
from ..viewsets.sitesetting_viewsets import sitesettingViewsets
from ..viewsets.privacypolicy_viewsets import privacypolicyViewsets
from ..viewsets.termandcondition_viewsets import termandconditionViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('sitesetting', sitesettingViewsets, basename="sitesettingViewsets")
router.register('termandcondition', termandconditionViewsets, basename="termandconditionViewsets")
router.register('privacypolicy', privacypolicyViewsets, basename="privacypolicyViewsets")
