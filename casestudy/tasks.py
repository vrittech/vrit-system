from celery import shared_task
from .models import CaseStudy
from django.utils import timezone

@shared_task
def publish_scheduled_case_study_task():
    scheduled_case_study = CaseStudy.objects.filter(
        status='scheduled',
        publish_date__lte=timezone.now().date()
    )
    for case_study in scheduled_case_study:
        case_study.publish_if_scheduled()

    return f"Published {scheduled_case_study.count()} scheduled case_study"
