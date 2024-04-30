from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MytokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['grupo_id'] = user.groups.first().id if user.groups.exists() else None
        token['grupo_nombre'] = user.groups.first().name if user.groups.exists() else None
        token['idSucursal'] = user.idSucursal.id if user.idSucursal else None
        token['sucursal'] = user.idSucursal.nombre if user.idSucursal else None
        token['permisoDscto'] = user.permisoDscto
        token['empresa'] = user.idSucursal.idEmpresa.nombre if user.idSucursal else None

        return token