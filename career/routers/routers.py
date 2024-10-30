from rest_framework.routers import DefaultRouter
from ..viewsets.expriencelevel_viewsets import expriencelevelViewsets
from ..viewsets.career_viewsets import careerViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('experience-level', expriencelevelViewsets, basename="expriencelevelViewsets")
router.register('career', careerViewsets, basename="careerViewsets")
