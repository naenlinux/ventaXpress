from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from .models import Compras, DetalleCompra, Almacen, AlmacenPrecioUM
from mantenedoresApp.models import Productos
from .serializers import ComprasSerializer, DetalleCompraSerializer, AlmacenSerializer, AlmacenPrecioUMSerializer
from rest_framework.response import Response
from mantenedoresApp.models import UnidadMedida
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
class StandarResulsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000

class ComprasViewSet(viewsets.ModelViewSet):
    queryset = Compras.objects.all().order_by('-fecha')
    serializer_class = ComprasSerializer
    filter_backends = [SearchFilter]
    search_fields = ['idProveedor__empresa']
    pagination_class = StandarResulsSetPagination

    def create(self, request, *args, **kwargs):
        data = request.data
        detalles_data = data.pop('detalles',[])

        try:
            with transaction.atomic():
                #validacion para crear la compra
                serializer = ComprasSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                compra = serializer.save()
                #validacion y creacion de los detalles de compra
                detalles = []
      
                for detalle_data in detalles_data:
                    detalle_data['idCompra'] = compra.id
                    detalle_serializer = DetalleCompraSerializer(data=detalle_data)
                    detalle_serializer.is_valid(raise_exception=True)
                    detalle = detalle_serializer.save()
                    detalles.append(detalle)

                    #actualizar stock de almacen
                    #recogemos el idProducto
                    producto_id = detalle_data.get('idProducto', None)
                    cantidad = detalle_data.get('cantidad', 0)
                    precio = detalle_data.get('precio', 0)
                    unidad_medida = UnidadMedida.objects.get(id = detalle_data.get('unidadMedida',None)) #instanceamos a unidadMedida

                    if producto_id is not None:
                        try:
                            almacen = Almacen.objects.get(idProducto=producto_id)
                            #actualizamos los campos
                            almacen.cantidad += cantidad
                            almacen.precioCompra = precio
                            almacen.total += (cantidad * unidad_medida.proporcion)
                            almacen.save()
                        except Almacen.DoesNotExist:
                            pass
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return JsonResponse({'error':e},status=500)

    # CODIGO PARA RECOGER EL LOS CAMPOS DE UN CAMPO FOREING KEY DE LA TABLA RELACIONADA
    def list(self, request, *args, **kwargs):
        # Obtenemos los productos del queryset
        queryset = self.filter_queryset(self.get_queryset())

        # Obtenemos la página actual de la solicitud
        page = self.paginate_queryset(queryset)

        if page is not None:
            # Inicializamos una lista para almacenar los datos de los productos
            compra_data = []


            for compras in page:
                # Obtenemos el nombre de la categoría asociada a cada producto
                nombre_empresa = compras.idProveedor.empresa if compras.idProveedor else None
            
                # Serializamos el producto y agregamos el nombre de la categoría al JSON
                serializer = self.get_serializer(compras)
                data = serializer.data
                data['empresa'] = nombre_empresa

                # Agregamos los datos del producto a la lista
                compra_data.append(data)

            # Devolvemos la lista de productos con los nombres de las categorías
            return self.get_paginated_response(compra_data)

        # Si no hay paginación, devolvemos el queryset sin modificar
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        #obtenemos el nombre del proveedor asociado a la compra
        nombre_proveedor = instance.idProveedor.empresa if instance.idProveedor else None
        nombre_comprob = instance.idTipoComprob.nombre if instance.idTipoComprob else None
        ruc = instance.idProveedor.ruc if instance.idProveedor else None

        serializer = self.get_serializer(instance)
        data = serializer.data
        data['proveedor'] = nombre_proveedor
        data['comprobante'] = nombre_comprob
        data['ruc'] = ruc

        return Response(data)

class DetalleCompraViewSet(viewsets.ModelViewSet):
    queryset = DetalleCompra.objects.filter(activo=1).order_by('-id')
    serializer_class = DetalleCompraSerializer
    

    def list(self, request, *args, **kwargs):
        id_compra = self.request.query_params.get('idCompra')
        if id_compra is not None:
            detalles = self.queryset.filter(idCompra=id_compra)

            for detalle in detalles:
                detalle.producto = detalle.idProducto.nombre

            serializer = self.get_serializer(detalles, many=True)
            return Response(serializer.data)
        return super().list(request, *args, **kwargs)
    
    #actualizamos el stock despues de ANULAR de compra
    def create(self, request, *args, **kwargs):
        detalles = request.data.get('detalles',[])
        id_compra = request.data.get('idCompra')

        try:
            with transaction.atomic():
                if id_compra:
                    compra =  Compras.objects.get(pk=id_compra)
                    compra.activo = 0
                    compra.save() #anulamos la compra

                    for detalle in detalles:
                        producto_id = detalle.get('idProducto')
                        cantidad = detalle.get('cantidad')
                        proporcion = detalle.get('proporcion')

                        try: #actualizar stock  de la tabla almacen luego de anular
                            almacen = Almacen.objects.get(idProducto=producto_id)
                            almacen.cantidad -= cantidad
                            almacen.total -= (cantidad * int(proporcion))
                            almacen.save()
                        except Almacen.DoesNotExist:
                            pass
        except Exception as e:
            print(e)
            return JsonResponse({'error':e},status=500)

        return Response({'message': 'Detalles de compra actualizados correctamente'})
        #return super().create(request, *args, **kwargs)

class AlmacenViewSet(viewsets.ModelViewSet):
    queryset = Almacen.objects.select_related('idProducto').all().order_by('-id')
    serializer_class = AlmacenSerializer
    filter_backends = [SearchFilter]
    search_fields = ['idProducto__nombre']
    pagination_class = StandarResulsSetPagination

    #codigo para ordenar una lista por GET
    def get_queryset(self):
        queryset = super().get_queryset()
        #obtener el parametro order de la solicitud GET
        order_parametro = self.request.query_params.get('ordenar', None)
        categoria_parametro = self.request.query_params.get('categoria', None)

        #si hay parametro de ordenar, ordenalo
        if order_parametro:
            queryset = queryset.order_by(order_parametro)
        
        if categoria_parametro and int(categoria_parametro) > 0:
            queryset = queryset.filter(idProducto__categoria = categoria_parametro)

        return queryset

        # CODIGO PARA RECOGER EL LOS CAMPOS DE UN CAMPO FOREING KEY DE LA TABLA RELACIONADA
    def list(self, request, *args, **kwargs):
        # Obtenemos los productos del queryset
        queryset = self.filter_queryset(self.get_queryset())

        # Obtenemos la página actual de la solicitud
        page = self.paginate_queryset(queryset)

        if page is not None:
            # Inicializamos una lista para almacenar los datos de los productos
            almacen_data = []


            for almacen in page:
                # Obtenemos el nombre de la categoría asociada a cada producto
                nombre_producto = almacen.idProducto.nombre if almacen.idProducto else None
                nombre_unimedida = almacen.idProducto.unidadMedida.nombre if almacen.idProducto.categoria else None
                proporcion_um = almacen.idProducto.unidadMedida.proporcion
                categoria = almacen.idProducto.categoria.nombre

                # Serializamos el producto y agregamos el nombre de la categoría al JSON
                serializer = self.get_serializer(almacen)
                data = serializer.data
                data['nombre_producto'] = nombre_producto
                data['nombre_unimedida'] = nombre_unimedida
                data['proporcion_um'] = proporcion_um
                data['categoria'] = categoria

                # Agregamos los datos del producto a la lista
                almacen_data.append(data)

            # Devolvemos la lista de productos con los nombres de las categorías
            return self.get_paginated_response(almacen_data)

        # Si no hay paginación, devolvemos el queryset sin modificar
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class AlmacenPrecioUMViewSet(viewsets.ModelViewSet):
    queryset = AlmacenPrecioUM.objects.all()
    serializer_class = AlmacenPrecioUMSerializer
  
def dashboard(request):
    return render(request,'index.html')