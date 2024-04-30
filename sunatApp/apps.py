from django.apps import AppConfig


class SunatappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sunatApp'

    def ready(self):
        import sunatApp.signals