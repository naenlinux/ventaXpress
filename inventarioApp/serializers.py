from rest_framework import serializers
from .models import Compras, DetalleCompra, Almacen, AlmacenPrecioUM
from mantenedoresApp.serializers import ProductosSerializer

class ComprasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compras
        fields = '__all__'

class DetalleCompraSerializer(serializers.ModelSerializer):
    producto = serializers.CharField(source='idProducto.nombre',read_only=True)
    proporcion = serializers.CharField(source='idProducto.unidadMedida.proporcion',read_only=True)
    producto_um = serializers.CharField(source='idProducto.unidadMedida.nombre',read_only=True)
    class Meta:
        model = DetalleCompra
        fields = '__all__'

class AlmacenPrecioUMSerializer(serializers.ModelSerializer):
    nombre_unidad_medida = serializers.CharField(source='idUnidadMed.nombre',read_only=True)
    proporcion = serializers.CharField(source='idUnidadMed.proporcion',read_only=True)
    class Meta:
        model = AlmacenPrecioUM
        fields = '__all__'

class AlmacenSerializer(serializers.ModelSerializer):
    #idProducto = ProductosSerializer()
    precios_um = AlmacenPrecioUMSerializer(source='almacenprecioum_set',many=True,read_only=True)
    class Meta:
        model = Almacen
        fields = '__all__'