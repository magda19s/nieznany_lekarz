from django.apps import AppConfig


class VisitsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'visits'
    import visits.schema_extensions  
    # def ready(self):
    #     from django_celery_beat.models import PeriodicTask, IntervalSchedule

    #     from .tasks import publish_visits_scheduled_in_one_hour

    #     schedule, created = IntervalSchedule.objects.get_or_create(
    #         every=15,
    #         period=IntervalSchedule.MINUTES,
    #     )

    #     PeriodicTask.objects.get_or_create(
    #         interval=schedule,
    #         name='Check visits every 15 mins',
    #         task='visits.tasks.publish_visits_scheduled_in_one_hour',
    #     )
