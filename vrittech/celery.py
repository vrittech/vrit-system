import os
from celery import Celery
from celery.schedules import crontab  # For advanced scheduling
from django.conf import settings
from celery.schedules import crontab, schedule 
import os
from datetime import timedelta
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vrittech.settings')

app = Celery('vrittech')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks from all installed apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Periodic task schedules
app.conf.beat_schedule = {
    # Auto-expire Forms (from the `forms` app)
    'auto-expire-forms-daily': {
        'task': 'forms.tasks.auto_expire_forms',
        # 'schedule': crontab(hour=0, minute=0),  # Runs daily at midnight
        'schedule': schedule(timedelta(seconds=1)),
        # 'schedule': crontab(minute='*'),  # Runs every minute
    },
    # Auto-expire Careers (from the `career` app)
    'auto-expire-careers-daily': {
        'task': 'career.tasks.auto_expire_careers',
        # 'schedule': crontab(hour=1, minute=0),  # Runs daily at 1:00 AM
        'schedule': schedule(timedelta(seconds=1)),
        # 'schedule': crontab(minute='*'),  # Runs every minute
    },
    # Publish Scheduled Blogs (from the `blog` app)
    'publish-scheduled-blogs-hourly': {
        'task': 'blog.tasks.publish_scheduled_blog_task',
        # 'schedule': crontab(minute=0),  # Runs hourly
        'schedule': schedule(timedelta(seconds=1)),
        # 'schedule': crontab(minute='*'),  # Runs every minute
    },
    # Publish Scheduled Case Studies (from the `casestudy` app)
    'publish-scheduled-case-studies-hourly': {
        'task': 'casestudy.tasks.publish_scheduled_case_study_task',
        # 'schedule': crontab(minute=30),  # Runs hourly at the 30th minute
        'schedule': schedule(timedelta(seconds=1)),
        # 'schedule': crontab(minute='*'),  # Runs every minute
    },
    # Send Newsletters (from the `newslettersubscription` app)
    'send-newsletter-emails-daily': {
        'task': 'newslettersubscription.tasks.send_newsletter_subscription_emails',
        # 'schedule': crontab(hour=6, minute=0),  # Runs daily at 6:00 AM
        'schedule': schedule(timedelta(seconds=1)),
        # 'schedule': crontab(minute='*'),  # Runs every minute
    },
}

# Debug Task (Optional)
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
