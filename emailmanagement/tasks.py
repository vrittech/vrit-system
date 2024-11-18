from celery import shared_task
from .models import EmailLog, EmailManagement, EmailLogRecipient
from django.utils.timezone import now, timedelta
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_scheduled_emails():
    """
    Task to send scheduled emails that are due.
    """
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
    """
    Task to generate email logs based on Email Management configurations.
    """
    email_templates = EmailManagement.objects.all()

    generated_count = 0
    for template in email_templates:
        # Check frequency and generate logs accordingly
        last_generated_time = EmailLog.objects.filter(subject=template.subject).order_by('-created_at').first()
        frequency_map = {
            'day': timedelta(days=template.frequency_per),
            'week': timedelta(weeks=template.frequency_per),
            'month': timedelta(days=30 * template.frequency_per),
            'year': timedelta(days=365 * template.frequency_per),
        }
        if last_generated_time:
            next_scheduled_time = last_generated_time.created_at + frequency_map[template.frequency]
        else:
            next_scheduled_time = now()

        if now() >= next_scheduled_time:
            recipients = EmailLogRecipient.objects.all()  # Replace with actual recipient logic
            for recipient in recipients:
                log = EmailLog.objects.create(
                    subject=template.subject,
                    purpose=template.purpose,
                    preview=template.body,
                    status='scheduled',
                    scheduled_at=now(),  # Replace with actual scheduling logic if needed
                )
                log.recipient.add(recipient)
                generated_count += 1

    logger.info(f"Generated {generated_count} email logs.")
    return f"Generated {generated_count} email logs."
