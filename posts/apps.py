from django.apps import AppConfig
from django.conf import settings


class PostConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "posts"

    # def ready(self):
    #     super().ready()
    #     if settings.SCHEDULER_DEFAULT:
    #         from .runapscheduler import Command

    #         Command.start(self)
