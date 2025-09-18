from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import Permission

from termsconditionsprivacypolicy.models import PrivacyPolicy, TermsConditions
from .models import NotificationPerUser, NotificationUser, CustomUser

from faqs.models import Faqs

from django.db import models

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
# Public models
FORCED_MODELS = {
    # "blog", "branding", "career", "certificate",
    # "course", "faqs", "industryallies",
    # "journey", "mentor", "moments", "privacypolicy",
    # "successstory", "termsconditions", "testimonial","duration",
    # "level","blogcateogry","blogtags","contact","batch",
    # "category","enrollment","forms","requestform","custompage"

    "faqs"

}

# Map of model names to actual models (for convenience)
VALID_TYPES = {
  
    "faqs": Faqs,
   
}

def notify_users(action, instance, module_name, model_name):
    """
    Create a Notification and NotificationUser entries for relevant users.
    Superusers always get it.
    Team members only get it if they have the required permission,
    unless the model is in FORCED_MODELS.
    """
    identifier = getattr(instance, 'slug', instance.id)
    title = f"{model_name.capitalize()} {action.capitalize()}"
    action_messages = {
        'created': f"A new {model_name} item was added in the {module_name} module.",
        'updated': f"The {model_name} item was updated in the {module_name} module.",
        'deleted': f"The {model_name} item was deleted from the {module_name} module."
    }
    message = action_messages.get(action, "Updated item in module.")

    # Get the 'view' permission for this model
    permission_codename = f'view_{model_name.lower()}'
    view_permission = Permission.objects.filter(codename=permission_codename)
    print("hell\ooooooooo")

    if model_name.lower() in FORCED_MODELS:
        print("forced vitra gayo")
        # Superusers + all team members (permission check skipped)
        users_with_permission = CustomUser.objects.filter(
            models.Q(is_superuser=True) |
            models.Q(team_member__isnull=False)
        )
    else:
        print("dfhgjh\g")
        # Superusers always included, team members only if they have the permission
#         users_with_permission = CustomUser.objects.filter(
#             models.Q(is_superuser=True) |
#             (
#     models.Q( 
#         models.Q(user_permissions__in=view_permission) |
#         models.Q(groups__permissions__in=view_permission)
#     )
# ))
# Superusers always included, team members only if they have the permission

        users_with_permission = CustomUser.objects.filter(
            models.Q(is_superuser=True) |
            (models.Q(team_member__isnull=False) & (
    models.Q(team_member__isnull=False) & (
        models.Q(user_permissions__in=view_permission) |
        models.Q(groups__permissions__in=view_permission)
    )
))
        )
        
    channel_layer = get_channel_layer()
    # Create the main notification
    notification = NotificationPerUser.objects.create(
        title=title,
        message=message,
        module_name=module_name,
        updated_id=str(identifier)
    )

    # Assign the notification to each user (no duplicates)
    for user in users_with_permission.distinct():
        notif_user =  NotificationUser.objects.create(
            notification=notification,
            user=user
        )
        # 🔥 Push real-time notification
        async_to_sync(channel_layer.group_send)(
            f"user_{user.id}",
            {
                "type": "notify",  # maps to notify() in consumer
                "content": {
                    "title": title,
                    "message": message,
                    "module_name": module_name,
                    "updated_id": str(identifier),
                    "time_stamp": notification.created_at.isoformat(),
                    "is_read": notif_user.is_read,
                },
            },
        )


@receiver(post_save)
def create_or_update_notification(sender, instance, created, **kwargs):
    app_label = instance._meta.app_label
    model_name = instance._meta.model_name

    for key, model_class in VALID_TYPES.items():
        if sender == model_class:
            action = 'created' if created else 'updated'
            notify_users(action, instance, app_label, model_name)


@receiver(post_delete)
def delete_notification(sender, instance, **kwargs):
    app_label = instance._meta.app_label
    model_name = instance._meta.model_name

    for key, model_class in VALID_TYPES.items():
        if sender == model_class:
            notify_users('deleted', instance, app_label, model_name)