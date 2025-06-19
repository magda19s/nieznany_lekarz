import pika
import json
from django.conf import settings
import requests
from visits.models import Visit, TimeSlot, Doctor



def get_patient_email_from_service(patient_id):

    url = f"{settings.AUTH_SERVICE_URL}/auth/patient/{patient_id}"
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

def send_visit_to_queue(visit_arg):
    visit_tmp = Visit.objects.get(id=visit_arg.id)
    patient_id = visit_tmp.patient_id 

        # Token serwisowy do kontaktu z auth
    patient_response = get_patient_email_from_service(patient_id)
    print("[DEBUG] Sending auth request with headers:", patient_response)
    # if not patient_response or "email" not in patient_response:
    #     print(f"[!] Could not fetch email for patient {patient_id}")
    #     return
    patient_email = patient_response.get("email")
    visit = Visit.objects.select_related('doctor', 'time_slot', 'time_slot__doctor').get(id=visit_arg.id)

    timeslot = visit.time_slot
    doctor = visit.doctor

    visit_date = timeslot.start.strftime("%d.%m.%Y")
    visit_time = timeslot.start.strftime("%H:%M")
    doctor_fullname = f"{doctor.first_name} {doctor.last_name}"
    doctor_specialization = doctor.specialization

    subject = "Appointment notification"
    message = (
        f"This is a reminder about your upcoming appointment.\n"
        f"Date: {visit_date}\n"
        f"Time: {visit_time}\n"
        f"Doctor: Dr. {doctor_fullname} ({doctor_specialization})\n"
        f"Please arrive at least 10 minutes early."
    )

    event = {
        "to": patient_email,
        "subject": subject,
        "message": message
    }

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='visit-notifications', durable=True)

    

    channel.basic_publish(
        exchange='',
        routing_key='visit-notifications',
        body=json.dumps(event),
        properties=pika.BasicProperties(delivery_mode=2),
    )

    connection.close()
