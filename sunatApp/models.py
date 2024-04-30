from django.db import models
from ventaApp.models import Ventas
# Create your models here.
class CodigoNotaCredito(models.Model):
    codigo_sunat = models.CharField(max_length=2,null=True)
    descripcion = models.CharField(max_length=70,null=True)
    activo = models.BooleanField(default=True)

class ResumenDiario(models.Model):
    serie = models.CharField(max_length=5, null=True)
    numero = models.CharField(max_length=10, null=True)
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)

class ResumenDiarioDetalle(models.Model):
    idResDia = models.ForeignKey(ResumenDiario, on_delete=models.CASCADE)
    idVenta = models.ForeignKey(Ventas, on_delete=models.CASCADE)