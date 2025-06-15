from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from .models import Visit
from .utils.visits_publisher import send_visit_to_queue


@shared_task
def my_task():
    print("Zadanie działa!")
    
# @shared_task
# def publish_visits_scheduled_in_one_hour():
#     now = timezone.now()
#     target_time = now + timedelta(hours=1)
#     visits = Visit.objects.filter(
#         scheduled_time__gte=target_time.replace(minute=0, second=0, microsecond=0),
#         scheduled_time__lt=target_time.replace(minute=15, second=0, microsecond=0)
#     ).order_by('scheduled_time')

#     for visit in visits:
#         send_visit_to_queue(visit)
