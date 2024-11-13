# signals.py

from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import Blog, BlogCategory

@receiver(post_save, sender=Blog)
def set_position_same_as_id(sender, instance, created, **kwargs):
    if created and instance.position != instance.id:
        instance.position = instance.id
        instance.save()

# Signal to remove deleted category from blogs
@receiver(post_delete, sender=BlogCategory)
def remove_deleted_category_from_blogs(sender, instance, **kwargs):
    # Get all blogs that contain the deleted category
    blogs_with_category = Blog.objects.filter(category=instance)
    for blog in blogs_with_category:
        # Remove the deleted category from each blog's categories
        blog.category.remove(instance)
