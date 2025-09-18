from rest_framework.routers import DefaultRouter
from ..viewsets.projectgroup_viewsets import projectgroupViewsets
from ..viewsets.projectlink_viewsets import projectlinkViewsets
from ..viewsets.project_viewsets import projectViewsets
from ..viewsets.projectservice_viewsets import projectserviceViewsets

router = DefaultRouter()
auto_api_routers = router


# router.register('project-category', projectgroupViewsets, basename="projectgroupViewsets")
# router.register('project-service', projectserviceViewsets, basename="projectserviceViewsets")
# router.register('project', projectViewsets, basename="projectViewsets")
# router.register('project-link', projectlinkViewsets, basename="projectlinkViewsets")
