from celery import shared_task
from .models import Blog
from django.utils.timezone import now, localtime
import logging

logger = logging.getLogger(__name__)

@shared_task
def publish_scheduled_blog_task():
    current_time = localtime(now())  # Convert UTC to local time based on Django settings
    logger.info(f"Task started at: {current_time}")

    # Filter blogs that are ready to be published
    scheduled_blogs = Blog.objects.filter(
        status='scheduled',
        publish_date__lte=current_time  # Match date and time for DateTimeField
    )
    logger.info(f"Query executed. Found {scheduled_blogs.count()} scheduled blogs ready for publishing.")

    published_count = 0
    for blog in scheduled_blogs:
        try:
            logger.info(f"Processing Blog ID: {blog.id}, Title: {blog.title}, Publish Date: {blog.publish_date}")
            # Update the status to 'published'
            blog.status = 'published'
            blog.save(update_fields=['status'])
            published_count += 1
            logger.info(f"Successfully published Blog ID: {blog.id}")
        except Exception as e:
            logger.error(f"Failed to publish Blog ID: {blog.id}, Error: {e}")

    logger.info(f"Task completed. Published {published_count} scheduled blogs.")
    return f"Published {published_count} scheduled blogs."
