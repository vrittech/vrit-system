from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta

from accounts.models import CustomUser
from django.contrib.auth.models import Group

class TeamMemberCategory(models.Model):
    name= models.CharField(max_length=250)

    def __str__(self):
        return f"{self.name}"


class TeamMemberInvitation(models.Model):
    sent_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True,null=True, related_name="team_member_invitation")
    email = models.EmailField(unique=True)  # invited person's email
    full_name = models.CharField(max_length=250, blank=True,null=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    category = models.ForeignKey(
        "TeamMemberCategory", null=True, blank=True, on_delete=models.SET_NULL
    )
    position = models.CharField(blank=True, null=True)
    groups = models.ManyToManyField(Group, blank=True)

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("cancelled", "Cancelled"),
        ("expired", "Expired"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    is_superuser = models.BooleanField(default=False)

    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    otp_expires_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_otp(self, otp_code: str):
        """Set OTP and auto-expiry (10 minutes)."""
        self.otp = otp_code
        self.otp_created_at = timezone.now()
        self.otp_expires_at = self.otp_created_at + timedelta(minutes=10)
        self.save(update_fields=["otp", "otp_created_at", "otp_expires_at"])

    def is_otp_valid(self, otp_code: str) -> bool:
        """Check if OTP matches and is not expired."""
        if not self.otp or not self.otp_expires_at:
            return False
        if timezone.now() > self.otp_expires_at:
            return False
        return self.otp == otp_code

    def __str__(self):
        return f"Invitation to {self.email} [{self.status}]"


class PendingTeamMember(models.Model):
    invitation = models.OneToOneField(
        TeamMemberInvitation, on_delete=models.CASCADE, related_name="pending_user"
    )
    email = models.EmailField()
    full_name = models.CharField(max_length=250)
    password = models.CharField(max_length=128)  # store hashed later
    profile_image = models.CharField(max_length=500, null=True, blank=True)  # URL or base64
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pending user: {self.email}"



class TeamMember(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="team_member")
    invitation = models.OneToOneField(
        TeamMemberInvitation, on_delete=models.SET_NULL, null=True, blank=True
    )
    category = models.ForeignKey(
        TeamMemberCategory, null=True, blank=True, on_delete=models.SET_NULL
    )
    position = models.CharField(blank=True, null=True)
    
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email