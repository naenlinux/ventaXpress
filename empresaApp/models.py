from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Empresa(models.Model):
    nombre = models.CharField(max_length=100,blank=True)
    nombre_comercial = models.CharField(max_length=100,blank=True)
    ruc = models.CharField(max_length=20,blank=True)
    logo = models.ImageField(upload_to='images/',blank=True,null=True)
    direccion = models.CharField(max_length=80,blank=True)
    ubigeo = models.CharField(max_length=15,blank=True)
    gerente = models.CharField(max_length=50,blank=True)
    correo = models.CharField(max_length=100,blank=True)
    telefono = models.CharField(max_length=15,blank=True)
    activo = models.BooleanField(default=True)
    urbanizacion = models.CharField(max_length=60,blank=True)
    ciudad = models.CharField(max_length=50,blank=True)
    departamento = models.CharField(max_length=60,blank=True)
    provincia = models.CharField(max_length=60,blank=True)
    distrito = models.CharField(max_length=60,blank=True)
    usuario_sunat = models.CharField(max_length=15,blank=True)
    clave_sunat = models.CharField(max_length=15,blank=True)


class Monedas(models.Model):
    nombre = models.CharField(max_length=20,blank=True)
    codigo = models.CharField(max_length=5,blank=True)
    simbolo = models.CharField(max_length=10,blank=True)
    activo = models.BooleanField(default=True)

class TipoComprobantes(models.Model):
    nombre = models.CharField(max_length=20,blank=True)
    codigoSunat = models.CharField(max_length=10,blank=True)
    activo = models.BooleanField(default=True)

class ComprobanteConfig(models.Model):
    tipocomprobante = models.OneToOneField(TipoComprobantes, on_delete=models.CASCADE, null=True)
    serie = models.CharField(max_length=10,blank=True)
    numerocont = models.IntegerField(blank=True)
    activo = models.BooleanField(default=True)

class Impuesto(models.Model):
    valor_porcentaje = models.IntegerField(default="18")

class EnviarSunat(models.Model):
    valor = models.BooleanField(default=False)

class Sucursal(models.Model):
    nombre = models.CharField(max_length=100,blank=True)
    direccion = models.CharField(max_length=100,blank=True)
    idEmpresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True)
    activo = models.BooleanField(default=True)

# agregando nuevo campo a la tabla auth_user
User.add_to_class('idSucursal', models.ForeignKey(Sucursal, on_delete=models.SET_NULL,null=True,blank=True))
User.add_to_class('permisoDscto', models.BooleanField(default=False))