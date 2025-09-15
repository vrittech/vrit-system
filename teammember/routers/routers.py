from rest_framework.routers import DefaultRouter

from teammember.viewsets.category_viewsets import TeamMemberCategoryViewSet
from teammember.viewsets.invitation_viewsets import TeamMemberInvitationViewSet
from ..viewsets.teammember_viewsets import TeamMemberViewSet  

router = DefaultRouter()
auto_api_routers = router


router.register('team-member', TeamMemberViewSet, basename="TeamMemberViewSet")
router.register('team-member-category', TeamMemberCategoryViewSet, basename="TeamMemberCategoryViewSet")

router.register('team-member-invitation', TeamMemberInvitationViewSet, basename="TeamMemberInvitationViewSet")
