from django.db.models.signals import post_migrate
from django.dispatch import receiver

from django.db import transaction

@receiver(post_migrate)
def create_initial_groups(sender, **kwargs):
    from django.contrib.auth.models import Group
    if not Group.objects.exists():
        # crear el grupo prederteminado CREAMOS LOS GRUPOS
        Group.objects.create(name='Aministrador')
        Group.objects.create(name='Cajero')
        Group.objects.create(name='Vendedor')
        Group.objects.create(name='CajaVenta')
        print('Administrador registrado con exito')

@receiver(post_migrate)
def create_initial_igv(sender, **kwargs):
    from .models import Impuesto
    if not Impuesto.objects.exists():
        # crear el grupo prederteminado CREAMOS LOS GRUPOS
        Impuesto.objects.create(valor_porcentaje = 18) #18% IGV

@receiver(post_migrate)
def create_initial_enviar_sunat(sender, **kwargs):
    from .models import EnviarSunat
    if not EnviarSunat.objects.exists():
        EnviarSunat.objects.create(valor = 0)

@receiver(post_migrate)
def create_initial_tipoComprobante(sender, **kwargs):
    from .models import TipoComprobantes
    if not TipoComprobantes.objects.exists():
        TipoComprobantes.objects.create(nombre = 'BOLETA DE VENTA', codigoSunat = '03')
        TipoComprobantes.objects.create(nombre = 'FACTURA', codigoSunat = '01')
        TipoComprobantes.objects.create(nombre = 'NOTA DE CREDITO', codigoSunat = '07')

@receiver(post_migrate)
def create_initial_moneda(sender, **kwargs):
    from .models import Monedas
    if not Monedas.objects.exists():
        Monedas.objects.create(nombre = 'NUEVO SOL', codigo = 'PEN', simbolo = 'S/')

# crear super usuario deshabilitado
''''
@receiver(post_migrate)
def create_default_users_and_groups(sender, **kwargs ):
    #verificar si las tablas auth_user y auth_group fueron creadas
    if sender.name == 'django.contrib.auth':
        # crear el usuario prederteminado
        if not User.objects.filter(username = 'naen').exists():
            # crear el super usuario
            User.objects.create_superuser('naen','naen@naen.com','jdz')
'''