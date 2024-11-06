# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CareerGallery

@receiver(post_save, sender=CareerGallery)
def set_position_same_as_id(sender, instance, created, **kwargs):
    if created and instance.position != instance.id:
        instance.position = instance.id
        instance.save()
