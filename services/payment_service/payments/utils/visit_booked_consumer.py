import json
import pika
from payments.models import Payment
from django.utils.timezone import now
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payment_service.settings')  # zamień na nazwę swojego projektu
django.setup()

def handle_visit_booked(ch, method, properties, body):
    data = json.loads(body)
    print("Received VisitBooked:", data)

    Payment.objects.create(
        visit_id=data['visitId'],
        amount=120.0,  # Możesz tu dodać lepszą logikę
        currency='PLN',
        status='unpaid'
    )

def start_consumer():
    print("===> Starting consumer")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    print("===> Connected to RabbitMQ")
    channel = connection.channel()
    channel.queue_declare(queue='visit_booked', durable=True)

    channel.basic_consume(queue='visit_booked', on_message_callback=handle_visit_booked, auto_ack=True)
    print("===> Waiting for messages")
    print('[*] Waiting for VisitBooked...')
    channel.start_consuming()