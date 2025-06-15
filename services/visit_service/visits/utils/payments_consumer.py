import json
import pika
from django.utils.timezone import now
from visits.models import Visit, TimeSlot, Doctor
import django
import os
import requests


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visit_service.settings')  # zamień na nazwę swojego projektu
django.setup()

import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.test import APIRequestFactory
from visits.views import PatientRetrieveView 
from decouple import config


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

def publish_email_event(email, subject, message):
    event = {
        "to": email,
        "subject": subject,
        "message": message
    }

    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue="email-queue", durable=True)

    channel.basic_publish(
        exchange="",
        routing_key="email-queue",
        body=json.dumps(event),
        properties=pika.BasicProperties(delivery_mode=2),
    )
    connection.close()

def handle_payment(ch, method, properties, body):
    data = json.loads(body)
    print("Received Payment:", data)

    visit_id = data['visitId']
    status_value = data['status']# domyślnie unpaid, jeśli brak

    visit = Visit.objects.get(id=visit_id)
    patient_id = visit.patient_id 

        # Token serwisowy do kontaktu z auth
    patient_response = get_patient_email_from_service(patient_id)
    print("[DEBUG] Sending auth request with headers:", patient_response)
    # if not patient_response or "email" not in patient_response:
    #     print(f"[!] Could not fetch email for patient {patient_id}")
    #     return
    patient_email = patient_response.get("email")
    # patient_name = patient_data.get("first_name")

    if not patient_email:
        patient_email = 'student.integracja123@gmail.com'
 
    try:
        visit = Visit.objects.select_related('doctor', 'time_slot', 'time_slot__doctor').get(id=visit_id)

        timeslot = visit.time_slot
        doctor = visit.doctor

        visit_date = timeslot.start.strftime("%d.%m.%Y")
        visit_time = timeslot.start.strftime("%H:%M")
        doctor_fullname = f"{doctor.first_name} {doctor.last_name}"
        doctor_specialization = doctor.specialization

        if status_value == 'paid':
            visit.status = 'paid'
            subject = "Payment completed"
            message = (
                f"Your appointment has been paid.\n"
                f"Date: {visit_date}\n"
                f"Time: {visit_time}\n"
                f"Doctor: dr {doctor_fullname} ({doctor_specialization})"
            )
        elif status_value == 'unpaid':
            visit.status = 'cancelled'
            subject = "Payment failed"
            message = (
                f"Your appointment has been cancelled due to lack of payment.\n"
                f"Date: {visit_date}\n"
                f"Time: {visit_time}\n"
                f"Doctor: dr {doctor_fullname} ({doctor_specialization})"
            )
        else:
            print(f"[!] Unknown status: {status_value}")
            return

        visit.save()
        print(f"[✓] Visit {visit_id} status updated to {visit.status}")

        publish_email_event(patient_email, subject, message)
        print(f"[✓] Email event sent for visit {visit_id}")

    except Visit.DoesNotExist:
        print(f"[!] Visit with id {visit_id} not found")


    
def start_payment_consumer():
    print("===> Starting consumer")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    print("===> Connected to RabbitMQ")
    channel = connection.channel()
    channel.queue_declare(queue='payment', durable=True)

    channel.basic_consume(queue='payment', on_message_callback=handle_payment, auto_ack=True)
    print("===> Waiting for messages")
    print('[*] Waiting for Payment...')
    channel.start_consuming()