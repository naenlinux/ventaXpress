import pdb
import os
import decimal
from django.db import transaction
from django.utils import timezone
#from django.shortcuts import render
from django.http import JsonResponse
from inventarioApp.models import Almacen
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from empresaApp.models import ComprobanteConfig, Empresa, EnviarSunat
from .models import Pedidos, PedidosDetalle, Ventas, NotaCredito
from rest_framework import viewsets, status, filters
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as django_filters
from .serializers import PedidosDetalleSerializer, PedidosSerializer, VentasSerializer, CajaSerializer, NotaCreditoSerializer
from sunatApp.views import GenerarXml, EnviarSunatXML

# Create your views here.
class StandarResulSetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 1000

class PedidosFilter(django_filters.FilterSet):
    numero = django_filters.CharFilter(field_name='numero')
    fecha = django_filters.DateFilter(field_name='fecha')

    class Meta:
        model = Pedidos
        fields = ['numero']

class PedidosViewSet(viewsets.ModelViewSet):
    queryset = Pedidos.objects.all().order_by('-id')
    serializer_class = PedidosSerializer
    pagination_class = StandarResulSetPagination
    filter_backends = [SearchFilter, django_filters.DjangoFilterBackend]
    filterset_class = PedidosFilter
    #search_fields = ['numero']

    def create(self, request, *args, **kwargs): #Registrar pedido
        try:
            with transaction.atomic():
                fecha_hoy = timezone.localdate()
                #print(f'hoy es: {fecha_hoy}')
                last_pedido = Pedidos.objects.filter(fecha=fecha_hoy).order_by('-numero').first()
                #print(f'datos print {last_pedido}')
                #pdb.set_trace()
                if last_pedido:
                    numero = last_pedido.numero + 1
                else:
                    numero = 1

                request.data['numero'] = numero #agregamos el numero al objeto de datos
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)

                #Registrar detalles del pedido
                detalles = request.data.get('detalles',[])  #conseguimos el detalle del request
                for detalle in detalles:
                    PedidosDetalle.objects.create(
                        #pedido = serializer.instance,
                        idPedido_id = serializer.instance.id,
                        idAlmacen_id = detalle['idAlmacen'],
                        producto = detalle['producto'],
                        precio = detalle['precio'],
                        cantidad = detalle['cantidad'],
                        umVenta = detalle['umVenta'],
                        importe = detalle['importe'],
                        descuento = detalle['descuento'],
                        proporcion = detalle['proporcionVentaUM'],
                    )

                    #actualizar Stock de ALMACEN
                    id_almacen = detalle.get('idAlmacen')
                    proporcionVentaUM = detalle.get('proporcionVentaUM')
                    cantidad = detalle.get('cantidad')
                    proporcionUM = detalle.get('proporcionUM')

                    if id_almacen is not None:
                        try:
                            almacen = Almacen.objects.get(id=id_almacen)
                            almacen.total -= (int(proporcionVentaUM) * cantidad)
                            almacen.cantidad = ( almacen.total  ) / (proporcionUM)
                            almacen.save()
                        except Almacen.DoesNotExist:
                            pass

                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return JsonResponse({'error':str(e)},status=500)

class PedidoDetalleViewSet(viewsets.ModelViewSet):
    queryset = PedidosDetalle.objects.all()
    serializer_class = PedidosDetalleSerializer

    def list(self, request, *args, **kwargs):
        id_pedido = request.query_params.get('idPedido')
        if id_pedido is not None:
            detalles = PedidosDetalle.objects.filter(idPedido_id=id_pedido)
            serializer = self.get_serializer(detalles,many=True)
            return Response(serializer.data)
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        detalles = request.data.get('detalles',[])
        idPedido =  request.data.get('idPedido')

        try:
            with transaction.atomic():
                if idPedido:
                    pedido = Pedidos.objects.get(pk=idPedido)
                    pedido.activo = 0
                    pedido.estado = 'Anulado'
                    pedido.save() #anulamos pedido

                    for detalle in detalles:
                        idAlmacen = detalle.get('idAlmacen')
                        cantidad = float(detalle.get('cantidad'))
                        proporcion = detalle.get('proporcion')
                        proporcionUM = detalle.get('proporcionUM')

                        try: #Actualizamos el stock de la tabla almacen al anular
                            almacen = Almacen.objects.get(pk=idAlmacen)
                            almacen.total += (int(proporcion) * decimal.Decimal(cantidad))
                            almacen.cantidad =  ( almacen.total  ) / int(proporcionUM)
                            almacen.save()
                        except Almacen.DoesNotExist:
                            pass
        except Exception as e:
            return JsonResponse({'error':str(e)},status=500)
        
        return Response({'message':'Pedido anulado'})
        #return super().update(request, *args, **kwargs)


class CajaViewSet(viewsets.ModelViewSet):
    queryset = Ventas.objects.filter(activo=1)
    serializer_class = CajaSerializer
    filter_backends=[SearchFilter]
    search_fields=['idPedido__id']

    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                tipComprobante = request.data['tipComprobante']
                print(f'id compro {tipComprobante}')
                
                getSerieNum = ComprobanteConfig.objects.get(tipocomprobante_id=tipComprobante)
                #print(f'lista comrpr {getSerieNum}')
                #pdb.set_trace()
                request.data['numComprobante'] = str(getSerieNum.numerocont)
                request.data['serie'] = getSerieNum.serie
                #print(f'serie: {getSerieNum.serie} y numero: {getSerieNum.numerocont}')
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)

                #actualizar numerador del contador
                getSerieNum.numerocont += 1
                getSerieNum.save()

                #actualizamos estado pedido
                pedido = Pedidos.objects.get(pk=request.data['idPedido'])
                pedido.estado = 'Pagado'
                pedido.save()
                
                # GENERAR EL XML DEL COMPROBANTE CON LA FIRMA DIGITAL Y ENVIAR A SUNAT
                sunat = GenerarXml()
                nombre_zip = sunat.generarXml(serializer.instance.id)
                
                siEnviaSunat = EnviarSunat.objects.get(pk=1)
                if siEnviaSunat.valor: # enviar a SUNAT si esta TRUE el valor enviar
                    sunatXml = EnviarSunatXML()
                    sunatXml.enviarSoapSunat(nombre_zip)

                headers= self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            #error_message = str(e)
            return JsonResponse({'error':str(e) },status=500)
        #return super().create(request, *args, **kwargs)

class VentasFilter(django_filters.FilterSet):
    serie = django_filters.CharFilter(field_name='serie')
    numComprobante = django_filters.CharFilter(field_name='numComprobante')

    class Meta:
        model = Ventas
        fields = ['numComprobante']

class VentasViewSet(viewsets.ModelViewSet):
    queryset = Ventas.objects.all().order_by('-id')
    serializer_class = VentasSerializer
    pagination_class = StandarResulSetPagination
    filter_backends = [SearchFilter, django_filters.DjangoFilterBackend]
    filterset_class = VentasFilter
    #search_fields = ['numComprobante']

    def list(self, request, *args, **kwargs):
        # obtener los datos de la consulta original
        queryset = self.filter_queryset(self.get_queryset())
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(page, many=True)

        if not Empresa.objects.exists():
            return Response({'error':'Registre una empresa'})
        
        empresa = Empresa.objects.get(pk=1) # para hacer el get del ruc

        

        #agregar campo adicional
        data = serializer.data
        for item in data:
            item['nombre_cdr'] = self.revisar_cdr(f"R-{empresa.ruc}-{item['comprobante_cod']}-{item['serie']}-{item['numComprobante']}.xml")
            item['nombre_xmlzip'] = self.revisar_zip(f"{empresa.ruc}-{item['comprobante_cod']}-{item['serie']}-{item['numComprobante']}.zip")

        #construir el paginate
        paginated_response = {
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'results': data
        }
        return Response(paginated_response)
    
    def revisar_cdr(self, nombre_cdr):
        path = 'comprobantes/'
        ruta_cdr = os.path.join(path,nombre_cdr)
        if os.path.exists(ruta_cdr):
            return nombre_cdr
        else:
            return ''
        
    def revisar_zip(self, nombre_zip):
        path = 'comprobantes/'
        ruta_cdr = os.path.join(path,nombre_zip)
        if os.path.exists(ruta_cdr):
            return nombre_zip
        else:
            return ''

    def create(self, request, *args, **kwargs):
        idVenta =  request.data.get('idVenta')
        motivo = request.data.get('motivo')
        idPedido = request.data.get('idPedido')
        try:
            with transaction.atomic():
                if idVenta:
                    venta = Ventas.objects.get(pk=idVenta)
                    venta.activo = 0
                    venta.observacion = motivo
                    venta.save() #anulamos pedido

                    pedido = Pedidos.objects.get(pk=idPedido)
                    pedido.estado = 'Pendiente'
                    pedido.save()
        except Exception as e:
            return JsonResponse({'error':str(e)},status=500)
        
        return Response({'message':'Pedido anulado'})
    
class ReporteVentasViewSet(viewsets.ModelViewSet):
    queryset = Ventas.objects.all().order_by('id')
    serializer_class = VentasSerializer
    filter_backends = [SearchFilter, django_filters.DjangoFilterBackend]

    def list(self, request, *args, **kwargs):
        # obtener los datos de la consulta original
        fini_str = request.GET.get('fini')
        ffin_str = request.GET.get('ffin')
        queryset = self.queryset.filter(fecha__range=(fini_str,ffin_str)).exclude(activo=0)
        
        serializer = self.get_serializer(queryset, many=True)

        if not Empresa.objects.exists():
            return Response({'error':'Registre una empresa'})
        
        empresa = Empresa.objects.get(pk=1) # para hacer el get del ruc        

        #agregar campo adicional
        data = serializer.data
        for item in data:
            item['nombre_cdr'] = self.revisar_cdr(f"R-{empresa.ruc}-{item['comprobante_cod']}-{item['serie']}-{item['numComprobante']}.xml")
            item['nombre_xmlzip'] = self.revisar_zip(f"{empresa.ruc}-{item['comprobante_cod']}-{item['serie']}-{item['numComprobante']}.zip")
        
        return Response({'results':data})
    
    def revisar_cdr(self, nombre_cdr):
        path = 'comprobantes/'
        ruta_cdr = os.path.join(path,nombre_cdr)
        if os.path.exists(ruta_cdr):
            return nombre_cdr
        else:
            return ''
        
    def revisar_zip(self, nombre_zip):
        path = 'comprobantes/'
        ruta_cdr = os.path.join(path,nombre_zip)
        if os.path.exists(ruta_cdr):
            return nombre_zip
        else:
            return ''

    def create(self, request, *args, **kwargs):
        idVenta =  request.data.get('idVenta')
        motivo = request.data.get('motivo')
        idPedido = request.data.get('idPedido')
        try:
            with transaction.atomic():
                if idVenta:
                    venta = Ventas.objects.get(pk=idVenta)
                    venta.activo = 0
                    venta.observacion = motivo
                    venta.save() #anulamos pedido

                    pedido = Pedidos.objects.get(pk=idPedido)
                    pedido.estado = 'Pendiente'
                    pedido.save()
        except Exception as e:
            return JsonResponse({'error':str(e)},status=500)
        
        return Response({'message':'Pedido anulado'})

class NotaCreditoViewSet(viewsets.ModelViewSet):
    queryset = NotaCredito.objects.all().order_by('-id')
    serializer_class = NotaCreditoSerializer
    pagination_class = StandarResulSetPagination
    filter_backends = [SearchFilter]
    search_fields = ['serieNumero']

    def list(self, request, *args, **kwargs):
        # obtener los datos de la consulta original
        queryset = self.filter_queryset(self.get_queryset())
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(page, many=True)

        if not Empresa.objects.exists():
            return Response({'error':'Registe antes su empresa'})
        
        empresa = Empresa.objects.get(pk=1) # para hacer el get del ruc

        #agregar campo adicional
        data = serializer.data
        for item in data:
            pass
            item['nombre_cdr'] = self.revisar_cdr(f"R-{empresa.ruc}-{item['comprobante_cod']}-{item['serie']}-{item['numComprobante']}.xml")
            item['nombre_xmlzip'] = self.revisar_zip(f"{empresa.ruc}-{item['comprobante_cod']}-{item['serie']}-{item['numComprobante']}.zip")

        #construir el paginate
        paginated_response = {
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'results': data
        }
        return Response(paginated_response)
    
    def revisar_cdr(self, nombre_cdr):
        path = 'comprobantes/'
        ruta_cdr = os.path.join(path,nombre_cdr)
        if os.path.exists(ruta_cdr):
            return nombre_cdr
        else:
            return ''
        
    def revisar_zip(self, nombre_zip):
        path = 'comprobantes/'
        ruta_cdr = os.path.join(path,nombre_zip)
        if os.path.exists(ruta_cdr):
            return nombre_zip
        else:
            return ''

    def create(self, request, *args, **kwargs): #Registrar pedido
        try:
            with transaction.atomic():
                fecha_hoy = timezone.localdate()
                
                getSerieNum = ComprobanteConfig.objects.select_related('tipocomprobante').get(tipocomprobante__codigoSunat='07') # 07 nota de credito
                serieAnulado = request.data['serieNumeroAnu']
                request.data['serie'] = serieAnulado[0]+getSerieNum.serie #extrae la primera letra del comproban anulado y concatena a la serie de la NC
                request.data['tipComprobante'] = getSerieNum.tipocomprobante.id
                request.data['numComprobante'] = getSerieNum.numerocont #agregamos el numero al objeto de datos

                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)

                #Anular Venta
                idVenta = request.data['idVenta']
                id_pedido = request.data['idPedido']

                venta = Ventas.objects.get(pk=idVenta)
                venta.activo = 2 # 2 nota credito
                venta.save()

                pedido = Pedidos.objects.get(pk=id_pedido)
                pedido.estado = 'Pendiente' # cambiamos el pago del pedido a pendiente
                pedido.save()

                #actualizar numerador del contador
                getSerieNum.numerocont += 1
                getSerieNum.save()

                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return JsonResponse({'error':str(e)},status=500)
