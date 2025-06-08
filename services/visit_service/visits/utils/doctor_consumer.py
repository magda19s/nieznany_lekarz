import json
import pika
from visits.models import Doctor
from django.utils.timezone import now
import django
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visit_service.settings')
django.setup()

def handle_doctor_register(ch, method, properties, body):
    data = json.loads(body)
    print("Received DoctorRegister:", data)

    Doctor.objects.create(
        doctor_id=data['id'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        specialization='Cardiologist',
        amount=150
    )

    
def start_doctor_consumer():
    print("===> Starting consumer")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    print("===> Connected to RabbitMQ")
    channel = connection.channel()
    channel.queue_declare(queue='register_doctor', durable=True)

    channel.basic_consume(queue='register_doctor', on_message_callback=handle_doctor_register, auto_ack=True)
    print("===> Waiting for messages")
    print('[*] Waiting for DoctorRegister...')
    channel.start_consuming()