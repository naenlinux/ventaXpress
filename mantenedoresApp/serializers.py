from rest_framework import serializers
from .models import Proveedores, Categorias, Productos, UnidadMedida

class ProveedoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedores
        fields = '__all__'

class CategoriasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorias
        fields = '__all__'

class UnidadMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadMedida
        fields = '__all__'

class ProductosSerializer(serializers.ModelSerializer):
    #categoria = CategoriasSerializer()
    #unidadMedida = UnidadMedidaSerializer()
    class Meta:
        model = Productos
        fields = '__all__'
