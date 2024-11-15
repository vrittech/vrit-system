from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now
from .models import EmailManagement, NewsLetterSubscription
from blog.models import Blog
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_newsletter_subscription_emails():
    """
    Sends newsletters to subscribers based on their selected categories.
    """
    # Fetch EmailManagement configurations for newsletters
    email_configs = EmailManagement.objects.filter(purpose='newsletter_subscription')

    sent_count = 0
    failed_count = 0

    for email_config in email_configs:
        # Get all subscribers for the associated category
        subscribers = NewsLetterSubscription.objects.filter(
            is_subscribed=True, category=email_config.blog_category
        ).distinct()

        for subscriber in subscribers:
            try:
                # Fetch the required number of blogs for the email
                blogs = Blog.objects.filter(category=email_config.blog_category)[:email_config.number_of_blog]

                # Prepare the email body
                blog_links = "\n".join(
                    [f"{blog.title}: {blog.get_absolute_url()}" for blog in blogs]
                )
                email_body = f"{email_config.body}\n\nFeatured Blogs:\n{blog_links}"

                # Send the email
                send_mail(
                    subject=email_config.subject,
                    message=email_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[subscriber.email],
                    fail_silently=False,
                )

                # Log the successful email
                logger.info(f"Newsletter sent to {subscriber.email}")
                sent_count += 1
            except Exception as e:
                logger.error(f"Failed to send newsletter to {subscriber.email}: {e}")
                failed_count += 1

    logger.info(f"Newsletter task completed: {sent_count} sent, {failed_count} failed.")
    return f"Sent: {sent_count}, Failed: {failed_count}"
