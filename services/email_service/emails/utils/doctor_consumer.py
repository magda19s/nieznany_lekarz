import json
import pika
from django.utils.timezone import now
import django
import os
from django.core.mail import send_mail
import logging
from emails.models import Email

logger = logging.getLogger(__name__)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'email_service.settings')  # zmień na swój projekt
django.setup()

def send_email_message(to, subject, message):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email='student.integracja123@gmail.com',
            recipient_list=[to],
            fail_silently=False,
        )
        logger.info(f"[EMAIL] Email sent to {to} with subject '{subject}'")
    except Exception as e:
        logger.error(f"[EMAIL] Failed to send email to {to}: {e}")
        raise

def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        to_email = data["to"]
        subject = data["subject"]
        message = data["message"]

        # Sprawdź czy mail już wysłany (status SENT)
        already_sent = Email.objects.filter(
            to=to_email,
            subject=subject,
            message=message,
            status='SENT'
        ).exists()

        if already_sent:
            logger.info(f"[SKIP] Email already sent to {to_email} with subject '{subject}'")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        send_email_message(to_email, subject, message)

        Email.objects.create(
            to=to_email,
            subject=subject,
            message=message,
            status='SENT',
            sent_at=now()
        )

        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.info(f"[✓] Email sent to {to_email}")

    except Exception as e:
        logger.error(f"[!] Failed to send email to {to_email if 'to_email' in locals() else 'unknown'}: {e}")

        Email.objects.create(
            to=to_email if 'to_email' in locals() else None,
            subject=subject if 'subject' in locals() else None,
            message=message if 'message' in locals() else None,
            status='FAILED',
            error_message=str(e),
            sent_at=now()
        )

        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def start_doctor_notification_email_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue="visit-notifications-doctor", durable=True)
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(queue="visit-notifications-doctor", on_message_callback=callback)
    logger.info("[*] Waiting for doctor email messages. To exit press CTRL+C")
    channel.start_consuming()
