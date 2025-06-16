import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visit_service.settings')

app = Celery('visits')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
