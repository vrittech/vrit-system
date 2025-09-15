from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from ..models import TeamMemberInvitation
from ..serializers.invitation_serializers import (
    InvitationAcceptSerializer,
    InvitationListSerializer,
    InvitationRetrieveSerializer,
    InvitationVerifyOtpSerializer,
    InvitationWriteSerializer,
)
from ..utilities.importbase import *
from rest_framework import permissions
from rest_framework.decorators import action
import uuid
from rest_framework.response import Response
from rest_framework import status

class TeamMemberInvitationViewSet(viewsets.ModelViewSet):
    serializer_class = InvitationListSerializer
    pagination_class = MyPageNumberPagination
    # permission_classes = [permissions.IsAuthenticated]

    queryset = TeamMemberInvitation.objects.all().order_by("-created_at")

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ["email", "status"]
    ordering_fields = ["id", "created_at", "status"]

    filterset_fields = {
        "id": ["exact"],
        "status": ["exact", "in"],
        "created_at": ["exact", "gte", "lte"],
    }

    def get_queryset(self):
        queryset = super().get_queryset().distinct().order_by("-created_at")
        return queryset

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return InvitationWriteSerializer
        elif self.action == "retrieve":
            return InvitationRetrieveSerializer
        return InvitationListSerializer
    

    @action(detail=True, methods=["post"])
    def resend_invite(self, request, pk=None):
        invitation = self.get_object()

        # generate new token and set status
        invitation.token = uuid.uuid4()
        invitation.status = "pending"
        invitation.save(update_fields=["token", "status"])

        # reuse serializer helper to send email
        serializer = InvitationWriteSerializer()
        serializer.send_invitation_email(invitation)

        return Response({"message": "Invitation resent successfully"})
    
    @action(detail=False, methods=["post"])
    def accept_invitation(self, request):
        serializer = InvitationAcceptSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create_pending_and_send_otp()
        return Response({"message": "OTP sent successfully"})
    

    @action(detail=False, methods=["post"])
    def resend_otp(self, request):
        token = request.data.get("token")
        email = request.data.get("email")

        if not token or not email:
            return Response({"error": "token and email are required"}, status=400)

        try:
            invitation = TeamMemberInvitation.objects.get(token=token, email=email, status="pending")
        except TeamMemberInvitation.DoesNotExist:
            return Response({"error": "Invalid or expired invitation"}, status=400)

        # reuse serializer helper to send OTP email
        serializer = InvitationAcceptSerializer()
        full_name = getattr(invitation.pending_user, "full_name", "User")
        serializer.send_otp_email(invitation, full_name)

        return Response({"message": "OTP resent successfully"})
    
    @action(detail=False, methods=["post"])
    def verify_otp(self, request):
        serializer = InvitationVerifyOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        team_member = serializer.create_user_from_pending()
        return Response(
            {"message": "OTP verified successfully, team member created", "team_member_id": team_member.id},
            status=status.HTTP_201_CREATED
        )
    

    