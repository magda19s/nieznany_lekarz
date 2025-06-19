import pika
import json
from django.conf import settings
import requests
from visits.models import Visit, TimeSlot, Doctor



def get_doctor_email_from_service(id):

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

def publish_doctor_schedule(doctor_visits, tomorrow):
    """
    Publikuje harmonogram wizyt dla lekarzy do kolejki RabbitMQ.

    doctor_visits: dict {doctor_obj: [Visit, Visit, ...], ...}
    tomorrow: datetime.date obiekt reprezentujący dzień harmonogramu
    """

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='visit-notifications-doctor', durable=True)

    for doctor, visits in doctor_visits.items():
        doctor_data = get_doctor_email_from_service(doctor.doctor_id)
        doctor_email = doctor_data.get("email") if doctor_data else None
        if not doctor_email:
            continue

        visit_lines = []
        for v in visits:
            time = v.time_slot.start.strftime('%H:%M')
            patient_data = get_doctor_email_from_service(v.patient_id)
            patient_name = patient_data.get("first_name") if patient_data else None
            patient_last_name = patient_data.get("last_name") if patient_data else None

            visit_lines.append(f"• {time} – Patient: {patient_name} {patient_last_name}")

        visit_list = "\n".join(visit_lines)
        subject = f"Schedule for {tomorrow.strftime('%d.%m.%Y')}"
        message = (
            f"Hello Dr. {doctor.first_name} {doctor.last_name},\n\n"
            f"Here is your appointment schedule for {tomorrow.strftime('%A, %d %B %Y')}:\n\n"
            f"{visit_list}\n\n"
            f"Have a great day!\nYour Clinic"
        )

        event = {
            "to": doctor_email,
            "subject": subject,
            "message": message
        }

        channel.basic_publish(
            exchange='',
            routing_key='visit-notifications-doctor',
            body=json.dumps(event),
            properties=pika.BasicProperties(delivery_mode=2),
        )

    connection.close()
