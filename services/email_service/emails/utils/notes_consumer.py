import json
import pika
from django.utils.timezone import now
import django
import os
from django.core.mail import send_mail
import logging
from emails.models import Email
from django.core.mail import EmailMessage

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO


logger = logging.getLogger(__name__)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'email_service.settings')  # zamień na nazwę swojego projektu
django.setup()

def generate_pdf(notes_text):
    buffer = BytesIO()

    # Ścieżka do czcionki wspierającej polskie znaki (DejaVuSans.ttf)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    pdfmetrics.registerFont(TTFont("DejaVu", font_path))

    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="Notes",
        fontName="DejaVu",
        fontSize=12,
        leading=16,
        alignment=TA_JUSTIFY,
    ))

    story = []

    story.append(Paragraph("Visit recommendations:", styles["Heading2"]))
    story.append(Paragraph(notes_text.replace("\n", "<br/>"), styles["Notes"]))

    doc.build(story)
    buffer.seek(0)
    return buffer

def send_email_with_pdf(to_email, subject, message, pdf_buffer):
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email='student.integracja123@gmail.com',
        to=[to_email],
    )
    email.attach("visit_notes.pdf", pdf_buffer.read(), "application/pdf")
    email.send(fail_silently=False)
    logger.info(f"[✓] Email sent to {to_email} with PDF attachment")

def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        to_email = data["to"]
        subject = data["subject"]
        message = data["message"]
        notes = data["notes"]

        # SPRAWDZENIE: czy już istnieje taki email w bazie
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

        # WYSYŁKA
# GENERUJEMY PDF z notes_text
        pdf_buffer = generate_pdf(notes)

        # WYSYŁKA
        send_email_with_pdf(to_email, subject, message, pdf_buffer)
        # ZAPIS DO BAZY
        Email.objects.create(
            to=to_email,
            subject=subject,
            message=message,
            status='SENT',
        )

        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f"[✓] Email sent to {to_email}")

    except Exception as e:
        logger.error(f"[!] Failed to send email to {to_email}: {e}")

        Email.objects.create(
            to=to_email if 'to_email' in locals() else None,
            subject=subject if 'subject' in locals() else None,
            message=message if 'message' in locals() else None,
            status='FAILED',
            error_message=str(e),
        )

        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def start_notes_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue="notes-publisher", durable=True)
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(queue="notes-publisher", on_message_callback=callback)
    print("[*] Waiting for email messages. To exit press CTRL+C")
    channel.start_consuming()
