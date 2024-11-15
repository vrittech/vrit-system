from celery import shared_task
from django.utils.timezone import now
from .models import CaseStudy
import logging

logger = logging.getLogger(__name__)

@shared_task
def publish_scheduled_case_study_task():
    current_time = now()
    logger.info(f"Task started at: {current_time}")

    # Filter case studies that are ready to be published
    scheduled_case_studies = CaseStudy.objects.filter(
        status='scheduled',
        publish_date__lte=current_time  # Matches date and time for DateTimeField
    )
    logger.info(f"Found {scheduled_case_studies.count()} scheduled case studies ready for publishing.")

    for case_study in scheduled_case_studies:
        try:
            case_study.status = 'published'  # Change the status to 'published'
            case_study.save(update_fields=['status'])
            logger.info(f"Published CaseStudy ID: {case_study.id}")
        except Exception as e:
            logger.error(f"Failed to publish CaseStudy ID {case_study.id}: {e}")

    return f"Published {scheduled_case_studies.count()} scheduled case studies."
