from django.core.management.base import BaseCommand
from visits.utils.payments_consumer import start_consumer

class Command(BaseCommand):
    help = "Consume VisitBooked events from RabbitMQ"

    def handle(self, *args, **kwargs):
        start_consumer()