import io
import os
import base64
import zipfile
import requests
import subprocess
from lxml import etree
from rest_framework import viewsets
from django.http import HttpResponse, JsonResponse
from empresaApp.models import Empresa, Impuesto
from rest_framework.views import APIView
from rest_framework.response import Response
from sunatApp.trama import TramaSOAPGenerator
from sunatApp.firmaDigital import FirmaDigital
from sunatApp.boletaFacturaXML import BoletaFacturaXML
from sunatApp.anularNCXML import AnularNCXML
from .models import CodigoNotaCredito
from .serializers import CodigoNotaCreditoSerializer
from ventaApp.models import Ventas, PedidosDetalle, NotaCredito

# Create your views here.
class GenerarXml(APIView):

    def get(self, request):
        if(request.GET.get('generar_xml')): # si la solicitud es para generar el XML
            id_venta = request.GET.get('id_venta')
            rpt_ge = self.generarXml(id_venta)
            if(rpt_ge):
                data_response = {'message':'success','mensaje': 'Xml generado'}
            else:
                data_response = {'message':'error','mensaje': 'Error al generar el XML'}
            return JsonResponse(data_response)

        if(request.GET.get('nombre_zip')): # descargar el xml ZIP
            nombre_zip = request.GET.get('nombre_zip')
            path_zip = os.path.join('comprobantes/',nombre_zip)
            if os.path.exists(path_zip):
                print(path_zip)
                # Abrimos el archivo y enviamos
                with open(path_zip, 'rb') as archivo:
                    contenido = archivo.read()
                    response = HttpResponse(contenido, content_type='application/zip')
                    response['Content-Disposition'] = f'attachment; filename="{nombre_zip}"'
                    return response
            else:
                print('NO hay el zip')
                return HttpResponse('No esxiste el archivo', status=404)
            
    def generarXml(self, id_venta):
        ventas = Ventas.objects.select_related('idPedido','tipComprobante').get(pk=id_venta)
        detalle_pedido = PedidosDetalle.objects.select_related('idAlmacen').filter(idPedido = ventas.idPedido.id)
        comprobSunat = ventas.tipComprobante.codigoSunat
        empresa = Empresa.objects.get(pk=1) # datos de empresa
        impuesto = Impuesto.objects.get(pk=1)
        
        xml_generator = BoletaFacturaXML(ventas,detalle_pedido,empresa,impuesto)
        nombre_comprobante = empresa.ruc+'-'+comprobSunat+'-'+ventas.serie+'-'+ventas.numComprobante
        xml_generator.generate_invoice_xml() #generar XML

        firma = FirmaDigital('invoice')
        firma.firmar_xml()
        
        #Comprimir comprobante xml firmado
        with open('comprobantes/xml/invoice_signed.xml', 'r', encoding='utf-8') as invoice_file:
            invoice_xml = invoice_file.read()
        
        directorio_save = "comprobantes/"
        os.makedirs(directorio_save, exist_ok=True)
        ruta_zip_completa = os.path.join(directorio_save, nombre_comprobante+'.zip')
        
        # Crear un archivo ZIP en memoria
        with io.BytesIO() as buffer_zip:
            with zipfile.ZipFile(buffer_zip, 'w', zipfile.ZIP_DEFLATED) as archivo_zip:
                archivo_zip.writestr(nombre_comprobante+'.xml', invoice_xml)
            
            #guardar el zip el el directorio destino
            with open(ruta_zip_completa, "wb") as archivo_final:
                archivo_final.write(buffer_zip.getvalue())

        return nombre_comprobante+'.zip'

class EnviarSunatXML(APIView):

    def get(self, request):
        if(request.GET.get('enviar_sunat')): # si la solicitud es para enviar a SUNAT
            nombre_xmlzip = request.GET.get('nombre_xmlzip')
            rpt_enviar = self.enviarSoapSunat(nombre_xmlzip)
            return JsonResponse(rpt_enviar)
        
        if(request.GET.get('nombre_cdr')): # descargar el xml CDR
            nombre_cdr = request.GET.get('nombre_cdr')
            path_cdr = os.path.join('comprobantes/',nombre_cdr)
            if os.path.exists(path_cdr):
                print(path_cdr)
                # Abrimos el archivo y enviamos
                with open(path_cdr, 'rb') as archivo:
                    contenido = archivo.read()
                    response = HttpResponse(contenido, content_type='application/zip')
                    response['Content-Disposition'] = f'attachment; filename="{nombre_cdr}"'
                    return response
            else:
                print('NO hay el cdr')
                return HttpResponse('No esxiste el archivo', status=404)

    def enviarSoapSunat(self,nombre_comprobante): #trama_xml
        #preparamos el ZIP
        ruta_archivo_zip = os.path.join("comprobantes/", nombre_comprobante)

        if os.path.exists(ruta_archivo_zip): #verificar si el archivo zip existe
            with open(ruta_archivo_zip, "rb") as archivo_zip: #leer el contenido
                contenido_zip = archivo_zip.read()
            
            zip_b64 = base64.b64encode(contenido_zip).decode("utf-8") # convertir archivo zip a 64, ubicamos el archivo recien guardado. 
        
        empresa = Empresa.objects.get(pk=1) # datos de empresa
        usuario = empresa.ruc+empresa.usuario_sunat
        clave = empresa.clave_sunat
        trama_xml = self.generar_trama_soap(usuario, clave, nombre_comprobante, zip_b64)


        url_servicio = "https://e-beta.sunat.gob.pe/ol-ti-itcpfegem-beta/billService" # Ruta del servicio SOAP para enviar BETA PRUEBA

        headers = { # Contenido de la trama XML
            "Content-Type": "text/xml", # Encabezados de la solicitud
        }
        try:
            response = requests.post(url_servicio, data=trama_xml, headers=headers) # Realizar la solicitud SOAP
            if response.status_code == 200: # Verificar si la solicitud fue exitosa (código de estado HTTP 200)
                respuesta_servicio = response.content # Obtener la respuesta del servicio
                
                # Procesar la respuesta como sea necesario
                # En este ejemplo, se devuelve la respuesta como una página HTML
                with open('comprobantes/RptaSunat/rpt_servicio.xml',"wb") as archivo: # guardamos las rpta
                    archivo.write(respuesta_servicio)            
                self.readRptaSunat()
                #return HttpResponse(respuesta_servicio, content_type="text/html")
                response_data = {
                    'message':'success',
                    'mensaje':'CDR recibido'
                }
                return response_data
            else:
                print(f"Respuesta del servidor SOAP: {response.text}")
                #return HttpResponse("La solicitud SOAP no fue exitosa.", status=500) # Manejar el caso en que la solicitud no fue exitosa
                response_data = {
                    'message':'error',
                    'mensaje':'Error al procesar'
                }
                return response_data
        except Exception as e:
            print(f"Error al enviar solicitud SOAP: {str(e)}")
            #return HttpResponse(f"Error en la solicitud SOAP: {str(e)}", status=500) # Manejar cualquier excepción que pueda ocurrir durante la solicitud
            response_data = {
                'message':'error',
                'mensaje':'Error al procesar'
            }
            return response_data
            

    def readRptaSunat(self):
        print('leyendo cdr')
      
        tree = etree.parse('comprobantes/RptaSunat/rpt_servicio.xml')

        root = tree.getroot() # Obtiene la raíz del árbol XML

        application_response_element = root.find(".//applicationResponse")

        rpt_b64_sunat = application_response_element.text
        decode = base64.b64decode(rpt_b64_sunat)

        with open('comprobantes/RptaSunat/cdr_comprobante.zip', 'wb') as cdr:
            cdr.write(decode)
        
        # DESCOMPRIMIR ZIP
        with zipfile.ZipFile('comprobantes/RptaSunat/cdr_comprobante.zip','r') as archivo_zip:
            archivo_zip.extractall('comprobantes/')

    def generar_trama_soap(self, username, password, file_name, zip_b64):
        trama_xml = f"""
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ser="http://service.sunat.gob.pe" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
                <soapenv:Header>
                <wsse:Security>
                <wsse:UsernameToken>
                <wsse:Username>{username}</wsse:Username>
                <wsse:Password>{password}</wsse:Password>
                </wsse:UsernameToken>
                </wsse:Security>
                </soapenv:Header>
                <soapenv:Body>
                <ser:sendBill>
                <fileName>{file_name}</fileName>
                <contentFile>{zip_b64}</contentFile>
                </ser:sendBill>
                </soapenv:Body>
                </soapenv:Envelope>
            """
        return trama_xml

class GenerarXmlNC(APIView):
    def get(self, request):
        id_notac = request.GET.get('id_notac')
        if(request.GET.get('generar_xmlnc')): #generar XML
            rpt_ge = self.generarNcXML(id_notac)
            if(rpt_ge):
                data_response = {'message':'success','mensaje': 'Xml generado'}
            else:
                data_response = {'message':'error','mensaje': 'Error al generar el XML'}
            return JsonResponse(data_response)

        if(request.GET.get('nombre_zip')): #Descargar ZIP
            nombre_zip = request.GET.get('nombre_zip')
            path_zip = os.path.join('comprobantes/',nombre_zip)
            if os.path.exists(path_zip):
                print(path_zip)
                # Abrimos el archivo y enviamos
                with open(path_zip, 'rb') as archivo:
                    contenido = archivo.read()
                    response = HttpResponse(contenido, content_type='application/zip')
                    response['Content-Disposition'] = f'attachment; filename="{nombre_zip}"'
                    return response
            else:
                print('NO hay el zip')
                return HttpResponse('No esxiste el archivo', status=404)
        
    def generarNcXML(self, id_notac):
        notaCredito = NotaCredito.objects.select_related('tipComprobante').get(pk=id_notac)

        ventas = Ventas.objects.select_related('idPedido','tipComprobante').get(pk=notaCredito.idVenta_id)
        detalle_pedido = PedidosDetalle.objects.select_related('idAlmacen').filter(idPedido = ventas.idPedido_id)
        comprobSunat = notaCredito.tipComprobante.codigoSunat
        empresa = Empresa.objects.get(pk=1) # datos de empresa
        impuesto = Impuesto.objects.get(pk=1)

        anular = AnularNCXML(empresa,notaCredito,ventas,detalle_pedido,impuesto)
        nombre_comprobante = empresa.ruc+'-'+comprobSunat+'-'+notaCredito.serie+'-'+notaCredito.numComprobante
        anular.generate_Xml_NC()

        firma = FirmaDigital('notaCredito')
        firma.firmar_xml()

        #Comprimir comprobante xml firmado
        with open('comprobantes/xml/notaCredito_signed.xml', 'r', encoding='utf-8') as invoice_file:
            invoice_xml = invoice_file.read()
        
        directorio_save = "comprobantes/"
        os.makedirs(directorio_save, exist_ok=True)
        ruta_zip_completa = os.path.join(directorio_save, nombre_comprobante+'.zip')
        
        # Crear un archivo ZIP en memoria
        with io.BytesIO() as buffer_zip:
            with zipfile.ZipFile(buffer_zip, 'w', zipfile.ZIP_DEFLATED) as archivo_zip:
                archivo_zip.writestr(nombre_comprobante+'.xml', invoice_xml)
            
            #guardar el zip el el directorio destino
            with open(ruta_zip_completa, "wb") as archivo_final:
                archivo_final.write(buffer_zip.getvalue())

        return nombre_comprobante+'.zip'

        #return JsonResponse({'message':'hola'})
        #return Response({'message':'Response'})

class NotaCreditoViewset(viewsets.ModelViewSet):
    queryset = CodigoNotaCredito.objects.all().filter(activo=1)
    serializer_class = CodigoNotaCreditoSerializer