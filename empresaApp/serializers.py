from rest_framework import serializers
from .models import Empresa, Monedas, TipoComprobantes, ComprobanteConfig, Impuesto, Sucursal, EnviarSunat
from django.contrib.auth.models import User, Group

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'

class MonedasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monedas
        fields = '__all__'

class TipoComprobantesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoComprobantes
        fields = '__all__'

class ComprobanteConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComprobanteConfig
        fields = '__all__'

class ImpuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Impuesto
        fields = '__all__'
        
class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class UsuariosSerializer(serializers.ModelSerializer):
    #groups = GroupSerializer(many=True, read_only=True)
    sucursal = serializers.CharField(source='idSucursal.nombre',read_only=True)
    class Meta:
        model = User
        fields = '__all__'

class EnviarSunatSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnviarSunat
        fields = '__all__'