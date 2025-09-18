from rest_framework.routers import DefaultRouter

from web_branding.viewsets.web_branding_viewsets import WebBrandingCategoryViewsets, positionViewsets, webBrandingViewsets

router = DefaultRouter()

router.register('web-branding', webBrandingViewsets, basename="webBrandingViewsets")
router.register('web-branding-position', positionViewsets, basename="positionViewsets")
router.register('web-branding-category', WebBrandingCategoryViewsets, basename="WebBrandingCategoryViewsets")
