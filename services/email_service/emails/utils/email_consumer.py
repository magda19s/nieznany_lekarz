import json
import pika
from django.utils.timezone import now
import django
import os
from django.core.mail import send_mail
import logging
from emails.models import EmailLog

logger = logging.getLogger(__name__)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'email_service.settings')  # zamień na nazwę swojego projektu
django.setup()

def send_email_message(to, subject, message):
    """
    Wysyła e-mail do wskazanego odbiorcy.
    Może być używana w konsumentach RabbitMQ.
    """
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

        send_email_message(to_email, subject, message)

        # Zapisz do bazy, że email został wysłany
        EmailLog.objects.create(
            to_email=to_email,
            subject=subject,
            message=message,
            status='sent',
        )

        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f"[✓] Email sent to {to_email}")
    except Exception as e:
        EmailLog.objects.create(
            to_email=to_email if 'to_email' in locals() else None,
            subject=subject if 'subject' in locals() else None,
            message=message if 'message' in locals() else None,
            status='failed',
        )

        print(f"[!] Failed to send email: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def start_email_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue="email-queue", durable=True)
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(queue="email-queue", on_message_callback=callback)
    print("[*] Waiting for email messages. To exit press CTRL+C")
    channel.start_consuming()
