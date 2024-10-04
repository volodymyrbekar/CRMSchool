from django.apps import AppConfig


class CentersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'centers'

    def ready(self):
        import centers.signals  # Ensure the signals are imported