from rest_framework.routers import DefaultRouter
from ..viewsets.faqs_viewsets import faqsCategoryViewsets, faqsViewsets
from ..viewsets.contactus_viewsets import contactusViewsets

router = DefaultRouter()
auto_api_routers = router


router.register('faqs', faqsViewsets, basename="faqsViewsets")
router.register('faqs-category', faqsCategoryViewsets, basename="faqsCategoryViewsets")
router.register('contactus', contactusViewsets, basename="contactusViewsets")
