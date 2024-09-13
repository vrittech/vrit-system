from rest_framework.routers import DefaultRouter
from ..viewsets.testimonial_viewsets import testimonialViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('testimonial', testimonialViewsets, basename="testimonialViewsets")
