from celery import shared_task
from .models import EmailLog, EmailManagement
from django.utils.timezone import now
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_scheduled_emails():
    # Fetch scheduled emails that are due
    due_emails = EmailLog.objects.filter(status='scheduled', scheduled_at__lte=now())

    sent_count = 0
    failed_count = 0
    for email in due_emails:
        try:
            email.send_email()
            sent_count += 1
        except Exception as e:
            logger.error(f"Failed to send email {email.id}: {e}")
            failed_count += 1

    logger.info(f"Scheduled email task: {sent_count} sent, {failed_count} failed.")
    return f"Sent: {sent_count}, Failed: {failed_count}"


@shared_task
def generate_email_logs():
    # Generate Email Logs based on Email Management configurations
    email_templates = EmailManagement.objects.all()

    generated_count = 0
    for template in email_templates:
        # Logic for creating email logs
        log = EmailLog.objects.create(
            subject=template.subject,
            purpose=template.purpose,
            recipient="example@example.com",  # Replace with real logic for recipients
            preview=template.body,
            status='scheduled',
            scheduled_at=now(),  # Replace with actual scheduling logic
        )
        generated_count += 1

    logger.info(f"Generated {generated_count} email logs.")
    return f"Generated {generated_count} email logs."
