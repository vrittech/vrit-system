from celery import shared_task
from .models import Blog
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

@shared_task
def publish_scheduled_blogs_task():
    scheduled_blogs = Blog.objects.filter(
        status='scheduled',
        publish_date__lte=timezone.now()
    )
    published_count = 0
    for blog in scheduled_blogs:
        try:
            blog.publish_if_scheduled()
            published_count += 1
        except Exception as e:
            logger.error(f"Failed to publish blog ID {blog.id}: {e}")

    logger.info(f"Published {published_count} scheduled blogs.")
    return f"Published {published_count} scheduled blogs"
