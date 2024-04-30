from django.shortcuts import render
from rest_framework import viewsets, serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from .models import Proveedores, Categorias, Productos, UnidadMedida
from .serializers import ProveedoresSerializer, CategoriasSerializer, ProductosSerializer, UnidadMedidaSerializer
from inventarioApp.serializers import AlmacenSerializer
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from rest_framework.response import Response

# Create your views here.
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class ProveedoresViewSet(viewsets.ModelViewSet):
    queryset = Proveedores.objects.filter(activo='1').order_by('-id')
    serializer_class = ProveedoresSerializer
    filter_backends = [SearchFilter]
    search_fields = ['empresa','ruc']
    pagination_class = StandardResultsSetPagination

class CategoriasViewSetOrderName(viewsets.ModelViewSet):
    queryset = Categorias.objects.filter(activo='1').order_by('nombre')
    serializer_class = CategoriasSerializer

class CategoriasViewSet(viewsets.ModelViewSet):
    queryset = Categorias.objects.filter(activo='1').order_by('-id')
    serializer_class = CategoriasSerializer
    filter_backends = [SearchFilter]
    search_fields = ['nombre']
    pagination_class = StandardResultsSetPagination

class allCategoriasViewSet(viewsets.ModelViewSet):
    queryset = Categorias.objects.filter(activo='1').order_by('nombre')
    serializer_class = CategoriasSerializer
    
class ProductosViewSet(viewsets.ModelViewSet):
    queryset = Productos.objects.filter().order_by('-id')
    serializer_class = ProductosSerializer
    filter_backends = [SearchFilter]
    search_fields = ['nombre','codigo']
    pagination_class = StandardResultsSetPagination

    # CODIGO PARA RECOGER EL LOS CAMPOS DE UN CAMPO FOREING KEY DE LA TABLA RELACIONADA
    def list(self, request, *args, **kwargs):
        # Obtenemos los productos del queryset
        queryset = self.filter_queryset(self.get_queryset())

        # Obtenemos la página actual de la solicitud
        page = self.paginate_queryset(queryset)

        if page is not None:
            # Inicializamos una lista para almacenar los datos de los productos
            productos_data = []


            for producto in page:
                # Obtenemos el nombre de la categoría asociada a cada producto
                nombre_categoria = producto.categoria.nombre if producto.categoria else None
                nombre_unimedida = producto.unidadMedida.nombre if producto.unidadMedida else None

                # Serializamos el producto y agregamos el nombre de la categoría al JSON
                serializer = self.get_serializer(producto)
                data = serializer.data
                data['nombre_categoria'] = nombre_categoria
                data['nombre_unimedida'] = nombre_unimedida

                # Agregamos los datos del producto a la lista
                productos_data.append(data)

            # Devolvemos la lista de productos con los nombres de las categorías
            return self.get_paginated_response(productos_data)

        # Si no hay paginación, devolvemos el queryset sin modificar
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        producto_serializer = self.serializer_class(data=request.data)
        producto_serializer.is_valid(raise_exception=True)
        producto_instance = producto_serializer.save()

        almacen_data = {
            'idProducto': producto_instance.id,
            'cantidad': 0,
            'total':0,
            'uniMedida': 'Uni/Kg',
            'precioCompra': 0,
        }
        almacen_serializer = AlmacenSerializer(data=almacen_data)
        almacen_serializer.is_valid(raise_exception=True)
        almacen_serializer.save()

        response_data = {
            'producto': producto_serializer.data,
            'almacen': almacen_serializer.data
        }

        # Envía una actualización a través de WebSocket
        '''channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "productos_grupo",
            {
                "type": "update.product",
                "message": {"producto_id": producto_instance.id, "accion": "creado"},
            },
        )'''
        
        return Response(response_data)
    
 
class UnidadMedidaViewSet(viewsets.ModelViewSet):
    queryset = UnidadMedida.objects.all().order_by('-id')
    serializer_class = UnidadMedidaSerializer
    filter_backends = [SearchFilter]
    search_fields = ['nombre']
    pagination_class = StandardResultsSetPagination

class UnidadMedidaViewSetAll(viewsets.ModelViewSet):
    queryset = UnidadMedida.objects.all().order_by('nombre')
    serializer_class = UnidadMedidaSerializer
