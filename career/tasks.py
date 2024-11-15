from celery import shared_task
from django.utils import timezone
from .models import Career

@shared_task
def auto_expire_careers():
    now = timezone.now()
    expired_careers = Career.objects.filter(
        enable_auto_expiration=True,
        expiration_date__lte=now,
        is_expired=False
    )

    for career in expired_careers:
        career.is_expired = True
        career.is_show = False  
        career.save()

    return f"Auto-expired {expired_careers.count()} careers."
