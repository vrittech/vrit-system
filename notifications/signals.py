# signals.py in notifications app
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from accounts.models import CustomUser
from .models import Notification

from django.utils import timezone
from django.contrib.auth.models import Permission
from accounts.models import CustomUser
from .models import Notification

MODEL_MAP = {
    'project': ('projects', 'Project'),
    'project-service': ('projects', 'ProjectService'),
    'project-group': ('projects', 'ProjectGroup'),
    'blog': ('blog', 'Blog'),
    'career': ('career', 'Career'),
    'case-study': ('casestudy', 'CaseStudy'),
    'clients': ('clients', 'Clients'),
    'faqs': ('faqs', 'Faq'),
    'forms': ('forms', 'Form'),
    'forms-category': ('forms', 'Category'),
    'plan': ('plan', 'Plan'),
    'testimonial': ('testimonial', 'Testimonial'),
    'department': ('department', 'Department'),
    'gallery': ('gallery', 'Gallery'),
    'social-media': ('socialmedia', 'SocialMedia'),
    'role': ('accounts', 'Group'),
}

def notify_users(action, instance, module_name, model_name):
    """
    Helper function to create notifications for users based on the action type.
    """
    # Determine identifier: slug if available, otherwise id
    identifier = getattr(instance, 'slug', instance.id)

    # Define messages based on action with model_name and identifier included
    action_messages = {
        'created': f"A new {model_name} item was added in the {module_name} module.",
        'updated': f"The {model_name} item was updated in the {module_name} module.",
        'deleted': f"The {model_name} item was deleted from the {module_name} module."
    }

    # Prepare notification details
    title = f"{model_name.capitalize()} {action.capitalize()}"
    message = action_messages[action]

    # Find users with view permission for this model
    permission_codename = f'view_{model_name.lower()}'
    view_permission = Permission.objects.filter(codename=permission_codename)
    users_with_permission = CustomUser.objects.filter(user_permissions__in=view_permission)

    # Create and assign the notification with the updated_id field
    notification = Notification.objects.create(
        title=title,
        message=message,
        module_name=module_name,
        updated_id=str(identifier)  # Set updated_id with identifier
    )
    notification.users.set(users_with_permission)
    notification.save()  # Save notification to retain the responses

@receiver(post_save)
def create_or_update_notification(sender, instance, created, **kwargs):
    """
    Signal handler for create and update events.
    """
    # Identify app label and model name from the instance
    app_label = instance._meta.app_label
    model_name = instance._meta.model_name

    # Loop through MODEL_MAP to check if the instance matches any entry
    for module_key, (mapped_app_label, mapped_model_name) in MODEL_MAP.items():
        if app_label == mapped_app_label and model_name.lower() == mapped_model_name.lower():
            # Determine action type
            action = 'created' if created else 'updated'
            notify_users(action, instance, app_label, model_name)

@receiver(post_delete)
def delete_notification(sender, instance, **kwargs):
    """
    Signal handler for delete events.
    """
    # Identify app label and model name from the instance
    app_label = instance._meta.app_label
    model_name = instance._meta.model_name

    # Loop through MODEL_MAP to check if the instance matches any entry
    for module_key, (mapped_app_label, mapped_model_name) in MODEL_MAP.items():
        if app_label == mapped_app_label and model_name.lower() == mapped_model_name.lower():
            # Call notify_users for deletion
            notify_users('deleted', instance, app_label, model_name)

