from django.db import models
from mantenedoresApp import models as man
from empresaApp import models as emp

# Create your models here.
class Compras(models.Model):
    idProveedor = models.ForeignKey(man.Proveedores,on_delete=models.CASCADE,)
    fecha = models.DateField(null=True)
    idTipoComprob = models.ForeignKey(emp.TipoComprobantes,on_delete=models.CASCADE)
    numeroComprob = models.CharField(max_length=10)
    compraTotal = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    activo = models.BooleanField(default=True)

class DetalleCompra(models.Model):
    idCompra = models.ForeignKey(Compras, on_delete=models.CASCADE)
    idProducto = models.ForeignKey(man.Productos, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10,decimal_places=2,null=True)
    activo = models.BooleanField(default=True)

class Almacen(models.Model):
    idProducto = models.OneToOneField(man.Productos, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10,decimal_places=1,null=True)
    total = models.DecimalField(max_digits=10,decimal_places=1,null=True) #total de producto por unidad
    uniMedida = models.CharField(max_length=20,null=True)
    precioCompra = models.DecimalField(max_digits=10,decimal_places=2,null=True)
    activo = models.BooleanField(default=True)

class AlmacenPrecioUM(models.Model):
    idAlmacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)
    idUnidadMed = models.ForeignKey(man.UnidadMedida, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10,decimal_places=2,null=True)


