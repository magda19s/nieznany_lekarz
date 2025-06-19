import pika
import json
import os
from datetime import datetime
import pytz
import pika
import json
from django.conf import settings
import requests

RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'rabbitmq')

def get_user_email_from_service(id):

    url = f"{settings.AUTH_SERVICE_URL}/auth/patient/{id}"
    headers = {
    }

    print("[DEBUG] Sending auth request with headers:", headers)

    try:
        response = requests.get(url, headers=headers, timeout=5)
        print("[DEBUG] Response status:", response.status_code)
        print("[DEBUG] Response body:", response.text)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"[!] Auth service returned {response.status_code}: {response.text}")
            return None
    except requests.RequestException as e:
        print(f"[!] Request to auth service failed: {e}")
        return None

def publish_visit_notes_event(visit):
    try:
        patient = get_user_email_from_service(visit.patient_id)
        if not patient:
            print(f"[!] Patient data not found for ID {visit.patient_id}")
            return

        patient_email = patient.get("email")
        patient_name = f"{patient.get('first_name', '')} {patient.get('last_name', '')}".strip()

        doctor = get_user_email_from_service(visit.doctor_id)
        doctor_name = f"{doctor.get('first_name', '')} {doctor.get('last_name', '')}".strip()
        visit_date = visit.time_slot.start.strftime("%d.%m.%Y")
        visit_notes = visit.notes or "No additional notes."

        subject = "Post-visit Recommendations"
        message = (
            f"Dear {patient_name},\n\n"
            f"Please find below the recommendations from your appointment on {visit_date}:\n\n"
            f"{visit_notes}\n\n"
            f"Best regards,\nDr. {doctor_name}"
        )

        payload = {
            "to": patient_email,
            "subject": subject,
            "message": message,
            "notes" : visit_notes,
        }

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue='notes-publisher', durable=True)

        channel.basic_publish(
            exchange='',
            routing_key='notes-publisher',
            body=json.dumps(payload),
            properties=pika.BasicProperties(delivery_mode=2)
        )

        print(f"[✓] Queued notes email to {patient_email}")
        connection.close()

    except Exception as e:
        print(f"[!] Failed to publish visit notes email: {e}")