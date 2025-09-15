from django.urls import path, include

from termsconditionsprivacypolicy.viewsets.privacypolicy_viewsets import PrivacyPolicyAPIView
from termsconditionsprivacypolicy.viewsets.termsconditions_viewsets import TermsConditionsAPIView


urlpatterns = [
    path('termsconditions', TermsConditionsAPIView.as_view()),
    path('privacypolicy',PrivacyPolicyAPIView.as_view(),name="token_obtain_pair"),

]