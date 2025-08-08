from django.apps import AppConfig

class TimelineConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "timeline"

    def ready(self):
        # Enable SQLite WAL & sane sync on connection
        from . import signals  # noqa: F401
