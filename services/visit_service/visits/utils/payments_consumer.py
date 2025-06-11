import json
import pika
from django.utils.timezone import now
from visits.models import Visit
import django
import os
import requests


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visit_service.settings')  # zamień na nazwę swojego projektu
django.setup()

import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status

def get_patient_email_from_service(request, patient_id):
    # Pobierz nagłówek autoryzacji z requesta
    auth_header = request.META.get("HTTP_AUTHORIZATION")
    if not auth_header:
        return Response({"detail": "Authorization header missing"}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Przygotuj URL do user service - przykładowy endpoint, dostosuj do swojego
    url = f"{settings.USER_SERVICE_URL}/auth/patient"

    headers = {
        "Authorization": auth_header
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            email = data.get("email")
            if not email:
                return Response({"detail": "Email not found for patient"}, status=status.HTTP_404_NOT_FOUND)
            return email  # zwracamy email jako string
        elif response.status_code == 404:
            return Response({"detail": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "Failed to fetch email from user service"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    except requests.RequestException:
        return Response({"detail": "Failed to contact user service"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

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

    patient_id = visit.patient_id

        # Token serwisowy do kontaktu z auth
    service_token = settings.INTERNAL_AUTH_TOKEN 
    patient_email = get_patient_email_from_service(patient_id, service_token)
    if not patient_email:
            print(f"[!] Could not fetch email for patient {patient_id}")
            return
 
    try:
        visit = Visit.objects.get(id=visit_id)
        if status_value == 'paid':
            visit.status = 'paid'
            subject = "Płatność zakończona"
            message = f"Twoja wizyta {visit.id} została opłacona."
            #w tym miejscu będzie puszczany publish do email service
        elif status_value == 'unpaid':
            visit.status = 'cancelled'
            subject = "Płatność nieudana"
            message = f"Twoja wizyta {visit.id} została anulowana z powodu braku płatności."
                        #w tym miejscu będzie puszczany publish do email service

        else:
            print(f"[!] Unknown payment status: {status_value}")
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