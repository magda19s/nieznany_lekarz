from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from .models import Visit
from .utils.visits_publisher import send_visit_to_queue

    
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
