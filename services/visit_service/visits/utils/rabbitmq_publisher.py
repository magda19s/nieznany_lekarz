import pika
import json
import os
from datetime import datetime
import pytz

RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'rabbitmq')

def publish_visit_booked_event(visit):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()

        channel.queue_declare(queue='visit_booked', durable=True)

        message = {
            "event": "VisitBooked",
            "visitId": str(visit.id),
            "doctorId": str(visit.doctor.doctor_id),
            "patientId": visit.patient_id,
            "timeSlot": {
                "id": str(visit.time_slot.id),
                "start": visit.time_slot.start.isoformat(),
                "end": visit.time_slot.end.isoformat(),
            },
            "amount" : float(visit.doctor.amount),
            "timestamp": datetime.now(pytz.timezone('Europe/Warsaw')).strftime("%d.%m.%Y %H:%M:%S")
        }

        channel.basic_publish(
            exchange='',
            routing_key='visit_booked',
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2)  # trwała wiadomość
        )

        print(f"[x] Sent VisitBooked event for visit {visit.id}")
        connection.close()

    except Exception as e:
        print(f"[!] Failed to send VisitBooked event: {e}")