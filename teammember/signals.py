from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import TeamMember

@receiver(post_delete, sender=TeamMember)
def delete_user_and_invitation(sender, instance, **kwargs):
    """
    When a TeamMember is deleted:
      - Delete the associated CustomUser
      - Delete the associated TeamMemberInvitation
    """
    # delete user
    if instance.user:
        instance.user.delete()

    # delete invitation
    if instance.invitation:
        instance.invitation.delete()