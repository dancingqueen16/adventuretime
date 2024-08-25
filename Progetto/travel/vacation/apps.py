from django.apps import AppConfig


class VacationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vacation'

    def ready(self):
        from django.contrib.sessions.models import Session
        Session.objects.all().delete()