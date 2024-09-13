from rest_framework.routers import DefaultRouter
from ..viewsets.features_viewsets import featuresViewsets
from ..viewsets.planhavefeatures_viewsets import planhavefeaturesViewsets
from ..viewsets.plan_viewsets import planViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('features', featuresViewsets, basename="featuresViewsets")
router.register('plan', planViewsets, basename="planViewsets")
router.register('plan-have-features', planhavefeaturesViewsets, basename="planhavefeaturesViewsets")
