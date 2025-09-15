from os import path
from rest_framework.routers import DefaultRouter

from termsconditionsprivacypolicy.viewsets.privacypolicy_viewsets import PrivacyPolicyAPIView
from termsconditionsprivacypolicy.viewsets.termsconditions_viewsets import termsConditionsViewsets



router = DefaultRouter()
auto_api_routers = router


# urlpatterns = [
#     path('privacypolicy/', PrivacyPolicyAPIView.as_view(), name='privacy-policy'),
# ]
# router.register('privacypolicy', PrivacyPolicyAPIView, basename="privacyPolicyViewsets")
# router.register('termsconditions', termsConditionsViewsets, basename="termsconditionsViewsets")


# urlpatterns += router.urls