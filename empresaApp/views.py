from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import Empresa, Monedas, TipoComprobantes, ComprobanteConfig, Impuesto, Sucursal, EnviarSunat
from .serializers import EmpresaSerializer, MonedasSerializer, TipoComprobantesSerializer, ComprobanteConfigSerializer, ImpuestoSerializer, SucursalSerializer, UsuariosSerializer, GroupSerializer, EnviarSunatSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User, Group
from django.http import Http404
from django.contrib.auth.hashers import make_password

# Create your views here.
class EmpresaViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = Empresa.objects.all().order_by('-id')
    serializer_class = EmpresaSerializer

    def create(self, request):
        serializer = EmpresaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    '''def list(self, request):
        serializer = EmpresaSerializer(self.queryset, many=True)
        return Response(serializer.data)'''


class MonedaViewset(viewsets.ModelViewSet):
    queryset = Monedas.objects.all().order_by('id')
    serializer_class = MonedasSerializer

class EnviarSunatViewset(viewsets.ModelViewSet):
    queryset = EnviarSunat.objects.all().order_by('id')
    serializer_class = EnviarSunatSerializer

class TipoComprobantesViewset(viewsets.ModelViewSet):
    #TipoComprobantes.objects.all().delete()
    queryset = TipoComprobantes.objects.all().order_by('id')
    serializer_class = TipoComprobantesSerializer

class ComprobanteConfigViewset(viewsets.ModelViewSet):
    queryset = ComprobanteConfig.objects.all().order_by('id')
    serializer_class = ComprobanteConfigSerializer

class ImpuestoViewset(viewsets.ModelViewSet):
    queryset = Impuesto.objects.all()
    serializer_class = ImpuestoSerializer
#class ImageUploadView(API)

class SucursalViewset(viewsets.ModelViewSet):
    queryset = Sucursal.objects.all().order_by('id')
    serializer_class = SucursalSerializer

    def create(self, request, *args, **kwargs):
        if not Empresa.objects.exists():
            return Response({'error':'Registre antes su empresa'}, status=400)
        return super().create(request, *args, **kwargs)

class UsuariosViewset(viewsets.ModelViewSet):
    queryset = User.objects.filter(id__gte=2).order_by('id')
    serializer_class = UsuariosSerializer

    def perform_create(self, serializer):
        try:
            grupos_ids = self.request.data.get('grupos', [])  # Obtén los IDs de los grupos del cuerpo de la solicitud
            usuario = serializer.save()  # Crea el usuario
            usuario.set_password(self.request.data.get('password'))
            usuario.save()
            for grupo_id in grupos_ids:
                grupo = Group.objects.get(pk=grupo_id)  # Obtiene el grupo por su ID
                usuario.groups.add(grupo)  # Agrega el usuario al grupo
        except Group.DoesNotExist:
            raise Http404("Uno o mas grupos no existen")
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        #instance = self.get_object()
        password = request.data.get('password')
        if password:
            hashed_password = make_password(password)
            request.data['password'] = hashed_password
        return super().update(request, *args, **kwargs)

class GruposViewset(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('id')
    serializer_class = GroupSerializer