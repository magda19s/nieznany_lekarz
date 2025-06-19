from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from .models import Visit
from .utils.visits_publisher import send_visit_to_queue
from .utils.doctor_visit_publisher import publish_doctor_schedule
from collections import defaultdict

    
@shared_task
def publish_visits_scheduled_in_one_hour():
    now = timezone.now()
    one_hour_later = now + timedelta(hours=1)

    visits = Visit.objects.filter(
        status__iexact='paid',
        time_slot__start__range=(now, one_hour_later)
    ).order_by('time_slot__start')

    for visit in visits:
        send_visit_to_queue(visit)

@shared_task
def send_doctor_schedule_for_next_day():
    tomorrow = timezone.localdate() + timedelta(days=1)
    start = timezone.make_aware(timezone.datetime.combine(tomorrow, timezone.datetime.min.time()))
    end = timezone.make_aware(timezone.datetime.combine(tomorrow, timezone.datetime.max.time()))

    # Pobierz wszystkie wizyty na jutro
    visits = Visit.objects.select_related('time_slot', 'doctor').filter(
        status__iexact='paid',
        time_slot__start__range=(start, end)
    ).order_by('time_slot__start')

    # Grupowanie wg lekarza
    doctor_visits = defaultdict(list)
    for visit in visits:
        doctor_visits[visit.doctor].append(visit)
    publish_doctor_schedule(doctor_visits, tomorrow)

