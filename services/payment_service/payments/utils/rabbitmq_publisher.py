import pika
import json
import os
from datetime import datetime
import pytz

RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'rabbitmq')

def publish_payment_event(payment):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()

        channel.queue_declare(queue='payment', durable=True)

        message = {
            "event": "Payment",
            "visitId": str(payment.visit_id),
            "status": str(payment.status),
            "amount": payment.amout,
            "currency": str(payment.currency),
            "timestamp": datetime.now(pytz.timezone('Europe/Warsaw')).strftime("%d.%m.%Y %H:%M:%S")
        }

        channel.basic_publish(
            exchange='',
            routing_key='payment',
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2)  # trwała wiadomość
        )

        print(f"[x] Sent Payment event for visit {payment.id}")
        connection.close()

    except Exception as e:
        print(f"[!] Failed to send Payment event: {e}")