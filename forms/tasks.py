from celery import shared_task
from django.utils.timezone import now
from .models import Forms
import logging

logger = logging.getLogger(__name__)

@shared_task
def auto_expire_forms():
    today = now().date()  # Get the current date
    forms_to_expire = Forms.objects.filter(
        auto_expiration=True,
        auto_expiration_date__lte=today,
        is_expired=False
    )

    expired_count = 0
    for form in forms_to_expire:
        try:
            form.is_expired = True
            form.is_show = False  # Optionally hide expired forms
            form.save()
            expired_count += 1
        except Exception as e:
            logger.error(f"Failed to expire form ID {form.id}: {e}")

    logger.info(f"Auto-expired {expired_count} forms.")
    return f"Auto-expired {expired_count} forms."
