import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vrittech.settings')

app = Celery('vrittech')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# Run the Celery worker:
# celery -A your_project worker --loglevel=info

# Run Celery Beat (to enable periodic tasks):
# celery -A your_project beat --loglevel=info
