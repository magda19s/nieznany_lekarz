import pika
import json
from django.conf import settings

def send_visit_to_queue(visit):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='visit_notifications', durable=True)

    message = {
        "visit_id": visit.id,
        "scheduled_time": visit.scheduled_time.isoformat(),
        "patient_id": visit.patient_id,
        "doctor_id": visit.doctor_id,
    }

    channel.basic_publish(
        exchange='',
        routing_key='visit_notifications',
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2),
    )

    connection.close()
