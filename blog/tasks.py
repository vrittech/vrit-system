from celery import shared_task
from .models import Blog
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

@shared_task
def publish_scheduled_blog_task():
    now = timezone.now()  # Get the current timestamp
    logger.info(f"Task started at: {now}")

    scheduled_case_studies = Blog.objects.filter(
        status='scheduled',
        publish_date__lte=now.date()  # Adjust for DateField
    )
    logger.info(f"Found {scheduled_case_studies.count()} scheduled case studies.")

    published_count = 0
    for blog in scheduled_case_studies:
        try:
            logger.info(f"Processing Blog ID: {blog.id}")
            # Update the status to 'published'
            blog.status = 'published'
            blog.save(update_fields=['status'])
            published_count += 1
            logger.info(f"Successfully published Blog ID: {blog.id}")
        except Exception as e:
            logger.error(f"Failed to publish Blog ID: {blog.id}: {e}")

    logger.info(f"Published {published_count} scheduled case studies.")
    return f"Published {published_count} scheduled case studies"
