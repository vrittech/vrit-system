from celery import shared_task
from .models import Blog
from django.utils import timezone

@shared_task
def publish_scheduled_blogs_task():
    scheduled_blogs = Blog.objects.filter(
        status='scheduled',
        publish_date__lte=timezone.now().date()
    )
    for blog in scheduled_blogs:
        blog.publish_if_scheduled()

    return f"Published {scheduled_blogs.count()} scheduled blogs"
