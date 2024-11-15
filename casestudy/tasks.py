from celery import shared_task
from .models import CaseStudy
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

@shared_task
def publish_scheduled_case_study_task():
    now = timezone.now()  # Get the current timestamp
    scheduled_case_studies = CaseStudy.objects.filter(
        status='scheduled',
        publish_date__lte=now
    )
    
    published_count = 0
    for case_study in scheduled_case_studies:
        try:
            # Update the status to 'published'
            case_study.status = 'published'
            case_study.save(update_fields=['status'])
            published_count += 1
            logger.info(f"Successfully published CaseStudy ID {case_study.id}")
        except Exception as e:
            logger.error(f"Failed to publish CaseStudy ID {case_study.id}: {e}")

    logger.info(f"Published {published_count} scheduled case studies.")
    return f"Published {published_count} scheduled case studies"
