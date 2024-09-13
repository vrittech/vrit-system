from rest_framework.routers import DefaultRouter
from ..viewsets.department_viewsets import departmentViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('department', departmentViewsets, basename="departmentViewsets")
