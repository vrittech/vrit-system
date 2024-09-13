from rest_framework.routers import DefaultRouter
from ..viewsets.casestudytags_viewsets import casestudytagsViewsets
from ..viewsets.casestudy_viewsets import casestudyViewsets
from ..viewsets.casestudycategory_viewsets import casestudycategoryViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('casestudy-tags', casestudytagsViewsets, basename="casestudytagsViewsets")
router.register('casestudy-category', casestudycategoryViewsets, basename="casestudycategoryViewsets")
router.register('casestudy', casestudyViewsets, basename="casestudyViewsets")
