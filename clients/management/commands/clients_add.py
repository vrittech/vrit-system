from django.core.management.base import BaseCommand
from ...models import Clients
import random
from faker import Faker

class Command(BaseCommand):
    help = 'Add 100 dummy clients'

    def handle(self, *args, **kwargs):
        fake = Faker()
        sections = ['first', 'second', 'third', 'fourth']

        for _ in range(100):
            name = fake.name()
            section = random.choice(sections)
            # If you want to use a dummy image, make sure to have an image file in the correct path
            media = None  # You can specify a path to an image file if needed
            position = random.randint(1, 9999)

            client = Clients.objects.create(
                name=name,
                section=section,
                media=media,
                position=position
            )
            self.stdout.write(self.style.SUCCESS(f'Client {client.name} added!'))
