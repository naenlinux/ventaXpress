from django.apps import AppConfig

class EmpresaappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'empresaApp'

    def ready(self):
        import empresaApp.signals