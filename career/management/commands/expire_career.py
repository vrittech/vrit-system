from django.core.management.base import BaseCommand
from career.models import Career
from datetime import date
from django.utils import timezone

class Command(BaseCommand):
    help = 'Mark careers as expired if the expiration date has passed'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        careers_to_expire = Career.objects.filter(
            enable_auto_expiration=True,
            expiration_date__lt=now,
            is_expired=False
        )

        careers_to_expire.update(is_expired=True, is_show=False)
        self.stdout.write(self.style.SUCCESS(f'{careers_to_expire.count()} careers marked as expired.'))

        today = date.today()
        forms_to_expire = Career.objects.filter(
            auto_expiration=True,
            auto_expiration_date__lt=today,
            is_expired=False
        )

        forms_to_expire.update(is_expired=True)
        self.stdout.write(self.style.SUCCESS(f'{forms_to_expire.count()} forms marked as expired.'))

# crontab -e
# 0 0 * * * /path/to/your/virtualenv/bin/python /path/to/your/project/manage.py expire_forms
# python manage.py expire_forms
# grep CRON /var/log/syslog
