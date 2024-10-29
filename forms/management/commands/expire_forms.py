from django.core.management.base import BaseCommand
from forms.models import Forms
from datetime import date

class Command(BaseCommand):
    help = 'Mark forms as expired if the auto expiration date has passed'

    def handle(self, *args, **kwargs):
        today = date.today()
        forms_to_expire = Forms.objects.filter(
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
