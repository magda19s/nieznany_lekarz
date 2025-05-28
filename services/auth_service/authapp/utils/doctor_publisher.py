import pika
import json
import os
from datetime import datetime
import pytz

RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'rabbitmq')

def publish_register_doctor_event(doctor):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()

        channel.queue_declare(queue='register_doctor', durable=True)

        message = {
            "event": "RegisterDoctor",
            "id": str(doctor.id),
            "email": str(doctor.email),
            "first_name": str(doctor.first_name),
            "last_name" : str(doctor.last_name),
            "timestamp": datetime.now(pytz.timezone('Europe/Warsaw')).strftime("%d.%m.%Y %H:%M:%S")
        }

        channel.basic_publish(
            exchange='',
            routing_key='register_doctor',
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2)  # trwała wiadomość
        )

        print(f"[x] Sent RegisterDoctor event for visit {doctor.id}")
        connection.close()

    except Exception as e:
        print(f"[!] Failed to send RegisterDoctor event: {e}")