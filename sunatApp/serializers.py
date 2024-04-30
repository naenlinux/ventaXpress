from rest_framework import serializers
from .models import CodigoNotaCredito

class CodigoNotaCreditoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodigoNotaCredito
        fields = '__all__'