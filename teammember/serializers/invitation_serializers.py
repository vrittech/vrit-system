from rest_framework import serializers

from accounts.models import CustomUser
from ..models import PendingTeamMember, TeamMember, TeamMemberCategory, TeamMemberInvitation
from django.conf import settings
from django.core.mail import EmailMessage
import random
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMemberCategory
        fields = ['id', 'name']

class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class InvitationListSerializer(serializers.ModelSerializer):
    category= CategorySerializer()
    class Meta:
        model = TeamMemberInvitation
        fields = ["id", "email", "status","category","groups", "created_at", "updated_at"]


class InvitationRetrieveSerializer(serializers.ModelSerializer):
    category= CategorySerializer()
    class Meta:
        model = TeamMemberInvitation
        fields = [
            "id",
            "email",
            "status",
            "otp_created_at",
            "otp_expires_at",
            "created_at",
            "updated_at",
            "token",
            "category",
            "groups"
        ]


class InvitationWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeamMemberInvitation
        fields = ["id", "email","is_superuser","category", "groups"]

    def send_invitation_email(self, invitation):
        frontend_base_url = getattr(settings, "FRONTEND_URL", "https://frontend-app.com")
        invite_url = f"{frontend_base_url}/accept-invite/?token={invitation.token}&email={invitation.email}"

        subject = "You're Invited to Join Our Team"
        body = f"""
        Hello,

        You have been invited to join our team.
        Please click the link below to accept the invitation:

        {invite_url}

        If you did not expect this invitation, you can ignore this email.
        """

        try:
            email = EmailMessage(
                subject=subject,
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[invitation.email],
            )
            email.send(fail_silently=False)
        except Exception as e:
            print("❌ Failed to send invitation email:", str(e))

    def create(self, validated_data):
        invitation = super().create(validated_data)
        # send email using helper
        self.send_invitation_email(invitation)
        return invitation
    


class InvitationAcceptSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    email = serializers.EmailField()
    full_name = serializers.CharField(max_length=250)
    password = serializers.CharField(write_only=True)
    profile_image = serializers.CharField(max_length=500, allow_blank=True, required=False)

    def validate(self, attrs):
        token = attrs.get("token")
        email = attrs.get("email")
        try:
            invitation = TeamMemberInvitation.objects.get(token=token, email=email, status="pending")
        except TeamMemberInvitation.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired invitation.")
        attrs["invitation_instance"] = invitation
        return attrs

    def create_pending_and_send_otp(self):
        invitation = self.validated_data["invitation_instance"]

        # create or update PendingTeamMember
        pending_user, created = PendingTeamMember.objects.update_or_create(
            invitation=invitation,
            defaults={
                "email": self.validated_data["email"],
                "full_name": self.validated_data["full_name"],
                "password": self.validated_data["password"],
                "profile_image": self.validated_data.get("profile_image", ""),
            },
        )

        # send OTP email
        self.send_otp_email(invitation, self.validated_data["full_name"])

        return pending_user

    def send_otp_email(self, invitation, full_name):
        # generate OTP and reset expiry
        otp_code = str(random.randint(100000, 999999))
        invitation.set_otp(otp_code)

        # send email
        subject = "Your OTP for Team Registration"
        body = f"""
        Hello {full_name},

        Your OTP code is: {otp_code}
        This code will expire in 10 minutes.

        If you did not request this, ignore this email.
        """
        try:
            email = EmailMessage(
                subject=subject,
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[invitation.email],
            )
            email.send(fail_silently=False)
        except Exception as e:
            print("❌ Failed to send OTP email:", str(e))




class InvitationVerifyOtpSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, attrs):
        token = attrs.get("token")
        email = attrs.get("email")
        otp = attrs.get("otp")

        # validate invitation
        try:
            invitation = TeamMemberInvitation.objects.get(token=token, email=email, status="pending")
        except TeamMemberInvitation.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired invitation.")

        if not invitation.is_otp_valid(otp):
            raise serializers.ValidationError("Invalid or expired OTP.")

        # validate pending user exists
        try:
            pending_user = invitation.pending_user
        except PendingTeamMember.DoesNotExist:
            raise serializers.ValidationError("No pending user found for this invitation.")

        attrs["invitation_instance"] = invitation
        attrs["pending_user_instance"] = pending_user
        return attrs

    def create_user_from_pending(self):
        invitation = self.validated_data["invitation_instance"]
        pending_user = self.validated_data["pending_user_instance"]

        # create CustomUser
        name_parts = pending_user.full_name.strip().split()
        if len(name_parts) == 0:
            first_name = ""
            last_name = ""
        elif len(name_parts) == 1:
            first_name = name_parts[0]
            last_name = ""
        else:
            first_name = " ".join(name_parts[:-1])  # everything except last word
            last_name = name_parts[-1]              # last word as last_name

        user = CustomUser.objects.create(
            email=pending_user.email,
            first_name=first_name,
            last_name=last_name,
            password=make_password(pending_user.password),
            professional_image=pending_user.profile_image,
            username=pending_user.email,
            is_superuser=invitation.is_superuser,
        )

        # Assign groups from invitation
        groups = invitation.groups.all()
        user.groups.set(groups)
        

        # create TeamMember
        team_member = TeamMember.objects.create(
            user=user,
            invitation=invitation
        )

        # update invitation status
        invitation.status = "accepted"

        invitation.save(update_fields=["status"])
        # link category
        if invitation.category:
            team_member.category = invitation.category
            team_member.save(update_fields=["category"])


        # delete pending user
        pending_user.delete()

        return team_member