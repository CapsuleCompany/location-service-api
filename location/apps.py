from django.apps import AppConfig
from django.db.models.signals import pre_migrate
from django.db import connection


class LocationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "location"

    def ready(self):
        pass