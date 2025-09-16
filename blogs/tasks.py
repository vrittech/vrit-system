from celery import shared_task
from django.utils.timezone import now
from celery.utils.log import get_task_logger
from .models import Blog

logger = get_task_logger(__name__)

@shared_task
def publish_scheduled_blogs():
    """
    Check all blogs that are scheduled and have a publish_date <= now,
    then update their status to 'published'.
    """
    current_time = now()  # Always timezone-aware UTC
    logger.info(f"[publish_scheduled_blogs] Started at {current_time} (UTC)")

    # Filter: status is scheduled + publish_date is set + publish_date <= now
    scheduled_blogs = Blog.objects.filter(
        status="scheduled",
        publish_date__isnull=False,
        publish_date__lte=current_time
    )

    if not scheduled_blogs.exists():
        logger.info("No scheduled blogs found to publish.")
        return "No scheduled blogs found."

    logger.info(f"Found {scheduled_blogs.count()} blogs ready to publish.")

    published_count = 0
    for blog in scheduled_blogs:
        try:
            logger.info(f"Publishing Blog ID={blog.id}, Title='{blog.title}', Publish Date={blog.publish_date}")
            blog.status = "published"
            blog.save(update_fields=["status"])
            published_count += 1
            logger.info(f"Blog ID={blog.id} successfully published.")
        except Exception as e:
            logger.error(f"Error publishing Blog ID={blog.id}: {e}")

    logger.info(f"Task completed. Published {published_count} blogs.")
    return f"Published {published_count} blogs."