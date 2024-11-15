from rest_framework.routers import DefaultRouter
from ..viewsets.category_viewsets import categoryViewsets
from ..viewsets.forms_viewsets import formsViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('forms-category', categoryViewsets, basename="categoryViewsets")
router.register('forms', formsViewsets, basename="formsViewsets")
