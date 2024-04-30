from rest_framework import serializers
from .models import Pedidos,PedidosDetalle,Ventas, NotaCredito
import os
from empresaApp.models import Empresa

class PedidosSerializer(serializers.ModelSerializer):
    usuario = serializers.CharField(source='idUsuario.username', read_only=True)
    comprobante = serializers.CharField(source='idComprob.nombre', read_only=True)
    moneda = serializers.CharField(source='idMoneda.nombre', read_only=True)
    sucursal = serializers.CharField(source='idSucursal.nombre',read_only=True)
    class Meta:
        model = Pedidos
        fields = '__all__'
    
class PedidosDetalleSerializer(serializers.ModelSerializer):
    proporcionUM = serializers.CharField(source='idAlmacen.idProducto.unidadMedida.proporcion',read_only=True)
    class Meta:
        model = PedidosDetalle
        fields = '__all__'

class VentasSerializer(serializers.ModelSerializer):
    subtotal = serializers.CharField(source='idPedido.subtotal',read_only=True)
    igv_total = serializers.CharField(source='idPedido.igv_total',read_only=True)
    comprobante = serializers.CharField(source='tipComprobante.nombre',read_only=True)
    comprobante_cod = serializers.CharField(source='tipComprobante.codigoSunat',read_only=True)
    numPedido = serializers.CharField(source='idPedido.numero',read_only=True)
    fechaPedido = serializers.CharField(source='idPedido.fecha',read_only=True)
    cliente = serializers.CharField(source='idPedido.cliente',read_only=True)
    cliente_doc = serializers.CharField(source='idPedido.cliente_doc',read_only=True)
    vendedor = serializers.CharField(source='idPedido.idUsuario.username',read_only=True)
    cobrador = serializers.CharField(source='idUsuario.username',read_only=True)
    moneda = serializers.CharField(source='idPedido.idMoneda.nombre',read_only=True)
    direccion = serializers.CharField(source='idPedido.cliente_dir', read_only=True)
    nombre_cdr= serializers.SerializerMethodField(read_only=True) #llamado automatico al metodo get_nombre_cdr
    nombre_zip= serializers.SerializerMethodField(method_name='get_nombre_zip', read_only=True) #llamado manual al metodo get_nombre_zip
    sucursal = serializers.CharField(source='idSucursal.nombre', read_only=True)
    dscto_total = serializers.CharField(source="idPedido.dscto_total",read_only=True)

    def get_nombre_cdr(self, obj):
        empre = Empresa.objects.get(pk=1)
        nombre_cdr = f"R-{empre.ruc}-{obj.tipComprobante.codigoSunat}-{obj.serie}-{obj.numComprobante}.xml"
        path = 'comprobantes/'
        ruta_cdr = os.path.join(path,nombre_cdr)
        if os.path.exists(ruta_cdr):
            return nombre_cdr
        else:
            return ''
    def get_nombre_zip(self, instance):
        empre = Empresa.objects.get(pk=1)
        nombre_zip = f"{empre.ruc}-{instance.tipComprobante.codigoSunat}-{instance.serie}-{instance.numComprobante}.zip"
        path = 'comprobantes/'
        ruta_cdr = os.path.join(path,nombre_zip)
        if os.path.exists(ruta_cdr):
            return nombre_zip
        else:
            return ''    
    
    class Meta:
        model = Ventas
        fields = '__all__'

class CajaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ventas
        fields = '__all__'

class NotaCreditoSerializer(serializers.ModelSerializer):
    serieAnulado = serializers.CharField(source='idVenta.serie',read_only=True)
    numeroAnulado = serializers.CharField(source='idVenta.numComprobante',read_only=True)
    comprobante_cod = serializers.CharField(source='tipComprobante.codigoSunat',read_only=True)
    class Meta:
        model = NotaCredito
        fields = '__all__'