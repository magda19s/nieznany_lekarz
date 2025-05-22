import json
import pika
from django.utils.timezone import now
from visits.models import Visit
import django
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visit_service.settings')  # zamień na nazwę swojego projektu
django.setup()

def handle_payment(ch, method, properties, body):
    data = json.loads(body)
    print("Received Payment:", data)

    visit_id = data['visitId']
    status_value = data['status']# domyślnie unpaid, jeśli brak

 
    try:
        visit = Visit.objects.get(id=visit_id)
        if status_value == 'paid':
            visit.status = 'paid'
        elif status_value == 'unpaid':
            visit.status = 'cancelled'
        else:
            print(f"[!] Unknown payment status: {status_value}")
            return

        visit.save()
        print(f"[✓] Visit {visit_id} status updated to {visit.status}")

    except Visit.DoesNotExist:
        print(f"[!] Visit with id {visit_id} not found")


    
def start_consumer():
    print("===> Starting consumer")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    print("===> Connected to RabbitMQ")
    channel = connection.channel()
    channel.queue_declare(queue='payment', durable=True)

    channel.basic_consume(queue='payment', on_message_callback=handle_payment, auto_ack=True)
    print("===> Waiting for messages")
    print('[*] Waiting for Payment...')
    channel.start_consuming()