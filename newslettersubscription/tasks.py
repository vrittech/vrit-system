from celery import shared_task
from emailmanagement.models import EmailManagement  # Correct location of the model
from newslettersubscription.models import NewsLetterSubscription
from blog.models import Blog
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_newsletter_subscription_emails():
    email_configs = EmailManagement.objects.filter(purpose='newsletter_subscription')

    for email_config in email_configs:
        subscribers = NewsLetterSubscription.objects.filter(
            is_subscribed=True, category=email_config.blog_category
        ).distinct()

        for subscriber in subscribers:
            try:
                send_mail(
                    subject=email_config.subject,
                    message=email_config.body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[subscriber.email],
                )
                logger.info(f"Email sent to {subscriber.email}")
            except Exception as e:
                logger.error(f"Failed to send email to {subscriber.email}: {e}")
