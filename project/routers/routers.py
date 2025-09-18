from rest_framework.routers import DefaultRouter

from project.viewsets.project_viewsets import caseStudyViewsets, projectCategoryViewsets, projectViewsets


router = DefaultRouter()
auto_api_routers = router


router.register('project', projectViewsets, basename="projectViewsets")
router.register('project-category', projectCategoryViewsets, basename="projectCategoryViewsets")
router.register('project-case-study', caseStudyViewsets, basename="caseStudyViewsets")
