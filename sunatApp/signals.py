from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_initial_igv(sender, **kwargs):
    from .models import CodigoNotaCredito
    if not CodigoNotaCredito.objects.exists():
        # crear el grupo prederteminado CREAMOS LOS GRUPOS
        CodigoNotaCredito.objects.create(codigo_sunat = '01', descripcion = 'Anulación de la operación') #18% IGV
