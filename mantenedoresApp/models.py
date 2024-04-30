from django.db import models

# Create your models here.
class Proveedores(models.Model):
    empresa = models.CharField(max_length=100, blank=True)
    ruc = models.CharField(max_length=30, blank=True)
    direccion = models.CharField(max_length=80, blank=True)
    correo = models.CharField(max_length=30, blank=True)
    telefono = models.CharField(max_length=12, blank=True)
    celular = models.CharField(max_length=12, blank=True)
    contacto = models.CharField(max_length=100, blank=True)
    activo = models.BooleanField(default=True)

class Categorias(models.Model):
    nombre = models.CharField(max_length=100,blank=True,unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

class UnidadMedida(models.Model):
    nombre = models.CharField(max_length=20,blank=True)
    nombrecorto = models.CharField(max_length=12,blank=True)
    proporcion = models.IntegerField(blank=True,null=True)
    unidadStock = models.CharField(max_length=10,blank=True)
    activo = models.BooleanField(default=True)

class Productos(models.Model):
    nombre = models.CharField(max_length=150,blank=True,unique=True)
    descripcion = models.TextField(blank=True)
    modelo = models.CharField(max_length=100,blank=True)
    codigo = models.CharField(max_length=8, null=True,unique=True,blank=True)
    activo = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE, null=True)
    unidadMedida = models.ForeignKey(UnidadMedida,on_delete=models.CASCADE,null=True)

