from rest_framework.routers import DefaultRouter
from ..viewsets.faqs_viewsets import faqsViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('faqs', faqsViewsets, basename="faqsViewsets")
