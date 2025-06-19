from django.core.management.base import BaseCommand
from emails.utils.notes_consumer import start_notes_consumer

class Command(BaseCommand):
    help = 'Starts the email RabbitMQ consumer'

    def handle(self, *args, **options):
        start_notes_consumer()
