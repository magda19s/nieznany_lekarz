from django.core.management.base import BaseCommand
from emails.utils.email_consumer import start_email_consumer

class Command(BaseCommand):
    help = 'Starts the email RabbitMQ consumer'

    def handle(self, *args, **options):
        start_email_consumer()
