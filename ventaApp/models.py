from django.db import models
from empresaApp import models as emp
from mantenedoresApp import models as man
from inventarioApp import models as inv
from django.contrib.auth.models import User


# Create your models here.
class Pedidos(models.Model):
    idUsuario = models.ForeignKey(User,on_delete=models.CASCADE)
    idComprob = models.ForeignKey(emp.TipoComprobantes,on_delete=models.CASCADE)
    cliente = models.TextField(max_length=100)
    cliente_doc = models.CharField(max_length=15,blank=True)
    cliente_dir = models.CharField(max_length=100,blank=True)
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    estado = models.CharField(max_length=20)
    numero = models.IntegerField(null=True)
    igv_total = models.DecimalField(max_digits=10,decimal_places=2,null=True)
    subtotal = models.DecimalField(max_digits=10,decimal_places=2,null=True)
    dscto_total = models.DecimalField(max_digits=10,decimal_places=2,null=True)
    idMoneda = models.ForeignKey(emp.Monedas,on_delete=models.CASCADE,null=True)
    idSucursal = models.ForeignKey(emp.Sucursal, on_delete=models.CASCADE,null=True)
    activo = models.BooleanField(default=True)

class PedidosDetalle(models.Model):
    idPedido = models.ForeignKey(Pedidos, on_delete=models.CASCADE,null=True)
    idAlmacen = models.ForeignKey(inv.Almacen,on_delete=models.CASCADE,null=True) #PRODUCTO
    producto = models.CharField(max_length=100,null=True)
    precio = models.DecimalField(max_digits=10,decimal_places=2,null=True)
    cantidad = models.DecimalField(max_digits=10,decimal_places=2,null=True)
    umVenta = models.CharField(max_length=50,null=True)
    proporcion = models.IntegerField(null=True) #CAMPO ESTA PARA QUE AL ANULAR EL PEDIDO SE RESTE EL STOCK
    importe = models.DecimalField(max_digits=10,decimal_places=2,null=True)
    descuento = models.IntegerField(null=True) # DESCUENTO EN PORCENTAJE
    activo = models.BooleanField(default=True)

class Ventas(models.Model):
    idUsuario = models.ForeignKey(User, on_delete=models.CASCADE)
    idPedido = models.ForeignKey(Pedidos,on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    tipComprobante = models.ForeignKey(emp.TipoComprobantes,on_delete=models.CASCADE)
    serie = models.CharField(max_length=5,null=True,blank=True)
    numComprobante = models.CharField(max_length=10)
    metodoPago = models.CharField(max_length=20,null=True)
    observacion = models.CharField(max_length=50,null=True,blank=True)
    idSucursal = models.ForeignKey(emp.Sucursal,on_delete=models.CASCADE, null=True)
    activo = models.IntegerField(default=1) # 0 eliminado, 1 activo, 2 nota de credito, 3 comunicacion de baja
    
class NotaCredito(models.Model):
    from sunatApp.models import CodigoNotaCredito
    idVenta = models.OneToOneField(Ventas, on_delete=models.CASCADE)
    tipComprobante = models.ForeignKey(emp.TipoComprobantes,on_delete=models.CASCADE)
    serie = models.CharField(max_length=5, blank=True)
    numComprobante = models.CharField(max_length=10,blank=True)
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    igv = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    motivo = models.CharField(max_length=100,blank=True)
    activo = models.BooleanField(default=True)
    codigoNC = models.ForeignKey(CodigoNotaCredito,on_delete=models.CASCADE,null=True)