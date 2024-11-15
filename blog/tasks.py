from celery import shared_task
from .models import Blog
from django.utils.timezone import now, localtime
import logging

logger = logging.getLogger(__name__)

@shared_task
def publish_scheduled_blog_task():
    # Get the current time in the timezone set in Django settings
    current_time = localtime(now())
    logger.info(f"Task started at: {current_time}")

    # Log to confirm the query conditions
    logger.info(f"Looking for blogs with publish_date <= {current_time} and status='scheduled'")

    # Query for scheduled blogs
    scheduled_blogs = Blog.objects.filter(
        status='scheduled',
        publish_date__lte=current_time  # Ensure publish_date is in the correct timezone
    )

    if scheduled_blogs.exists():
        logger.info(f"Found {scheduled_blogs.count()} scheduled blogs ready for publishing.")
    else:
        logger.info("No scheduled blogs found for the current time.")

    # Process each blog found
    published_count = 0
    for blog in scheduled_blogs:
        try:
            logger.info(f"Processing Blog ID: {blog.id}, Title: {blog.title}, Publish Date: {blog.publish_date}")
            # Change status to 'published'
            blog.status = 'published'
            blog.save(update_fields=['status'])
            published_count += 1
            logger.info(f"Successfully published Blog ID: {blog.id}")
        except Exception as e:
            logger.error(f"Failed to publish Blog ID: {blog.id}, Error: {e}")

    logger.info(f"Task completed. Published {published_count} scheduled blogs.")
    return f"Published {published_count} scheduled blogs."
