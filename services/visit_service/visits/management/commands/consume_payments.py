from django.core.management.base import BaseCommand
from visits.utils.payments_consumer import start_payment_consumer
from visits.utils.doctor_consumer import start_doctor_consumer

class Command(BaseCommand):
    help = "Consume events from RabbitMQ"

    def handle(self, *args, **kwargs):
        start_payment_consumer()