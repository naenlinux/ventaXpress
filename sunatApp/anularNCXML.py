from lxml import etree
from datetime import datetime
from decimal import Decimal
from num2words import num2words

class AnularNCXML:
    def __init__(self, empresa, notaCredtio, ventas, detalle_pedido, impuesto):
        self.empresa = empresa
        self.notaCredtio = notaCredtio
        self.ventas = ventas
        self.detalle_pedido = detalle_pedido
        self.impuesto = impuesto        

        self.namespaces = {
            None: "urn:oasis:names:specification:ubl:schema:xsd:CreditNote-2",
            'ext': "urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2",
            'cbc': "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
            'cac': "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
            'ds': "http://www.w3.org/2000/09/xmldsig#",
        }
    def generate_Xml_NC(self):
        notaCreditoRoot = etree.Element(
            "CreditNote",
            nsmap=self.namespaces       
        )
        etree.register_namespace('ds', 'http://www.w3.org/2000/09/xmldsig#')
        # UBLExtensions
        ubl_extensions = etree.SubElement(notaCreditoRoot, "{{{ext}}}UBLExtensions".format(ext=self.namespaces['ext']))
        ubl_extension = etree.SubElement(ubl_extensions, "{{{ext}}}UBLExtension".format(ext=self.namespaces['ext']))
        extension_content = etree.SubElement(ubl_extension, "{{{ext}}}ExtensionContent".format(ext=self.namespaces['ext']))
        # UBLVersionID
        cbc_UBLVersionID = etree.SubElement(notaCreditoRoot, "{{{cbc}}}UBLVersionID".format(cbc=self.namespaces['cbc']))
        cbc_UBLVersionID.text = "2.1"
         # CustomizationID
        cbc_CustomizationID = etree.SubElement(notaCreditoRoot, "{{{cbc}}}CustomizationID".format(cbc=self.namespaces['cbc']))
        cbc_CustomizationID.text = "2.0"
        # ID
        cbc_ID = etree.SubElement(notaCreditoRoot, "{{{cbc}}}ID".format(cbc=self.namespaces['cbc']))
        cbc_ID.text = self.notaCredtio.serie+'-'+self.notaCredtio.numComprobante  # "NC01-1" Numero de NOTA CREDI
        # IssueDate
        cbc_IssueDate = etree.SubElement(notaCreditoRoot, "{{{cbc}}}IssueDate".format(cbc=self.namespaces['cbc']))
        cbc_IssueDate.text = str(self.notaCredtio.fecha) # 2020-07-21 fecha de la NC
        cbc_IssueTime = etree.SubElement(notaCreditoRoot, "{{{cbc}}}IssueTime".format(cbc=self.namespaces['cbc']))
        hora_obj = datetime.strptime(str(self.notaCredtio.hora),"%H:%M:%S.%f")
        cbc_IssueTime.text = hora_obj.strftime("%H:%M:%S") #22:38:21 hora
        # Note
        cbc_Note = etree.SubElement(notaCreditoRoot, "{{{cbc}}}Note".format(cbc=self.namespaces['cbc']))
        cbc_Note.set("languageLocaleID", "1000")
        total_venta = self.notaCredtio.subtotal + self.notaCredtio.igv

        valor_entera = int(total_venta)
        valor_entera_palabra = num2words(valor_entera, lang='es').capitalize() # convertir el valor entero a palabra
        centavos = int((total_venta - valor_entera) * 100)
        centavos_palabra = num2words(centavos, lang='es').capitalize() # convertir los centavos en palabras

        cdata_note_text = f"{valor_entera_palabra.upper()} CON {centavos_palabra.upper()} /100 SOLES"
        cbc_Note.text = etree.CDATA(cdata_note_text)
        # DocumentCurrencyCode
        cbc_DocumentCurrencyCode = etree.SubElement(notaCreditoRoot, "{{{cbc}}}DocumentCurrencyCode".format(cbc=self.namespaces['cbc']))
        cbc_DocumentCurrencyCode.text = "PEN"
        #DiscrepancyResponse
        cac_DiscrepancyResponse = etree.SubElement(notaCreditoRoot, "{{{cac}}}DiscrepancyResponse".format(cac=self.namespaces['cac']))
        cbc_ReferenceID = etree.SubElement(cac_DiscrepancyResponse,"{{{cbc}}}ReferenceID".format(cbc=self.namespaces['cbc']))
        cbc_ReferenceID.text = self.ventas.serie+'-'+self.ventas.numComprobante # comprobante afectado
        cbc_ResponseCode = etree.SubElement(cac_DiscrepancyResponse,"{{{cbc}}}ResponseCode".format(cbc=self.namespaces['cbc']))
        cbc_ResponseCode.text = self.notaCredtio.codigoNC.codigo_sunat #codigo del tipo de nota de credito
        cbc_Description = etree.SubElement(cac_DiscrepancyResponse,"{{{cbc}}}Description".format(cbc=self.namespaces['cbc']))
        cbc_Description.text = self.notaCredtio.motivo # DEVOLUCION POR ITEM
        #BillingReference
        cac_BillingReference = etree.SubElement(notaCreditoRoot,"{{{cac}}}BillingReference".format(cac=self.namespaces['cac']))
        cac_InvoiceDocumentReference = etree.SubElement(cac_BillingReference,"{{{cac}}}InvoiceDocumentReference".format(cac=self.namespaces['cac']))
        cbc_ID = etree.SubElement(cac_InvoiceDocumentReference,"{{{cbc}}}ID".format(cbc=self.namespaces['cbc']))
        cbc_ID.text = self.ventas.serie+'-'+self.ventas.numComprobante
        cbc_DocumentTypeCode = etree.SubElement(cac_InvoiceDocumentReference,"{{{cbc}}}DocumentTypeCode".format(cbc=self.namespaces['cbc']))
        cbc_DocumentTypeCode.text = self.ventas.tipComprobante.codigoSunat #01 factura 03 boleta
        #DespatchDocumentReference
        '''cac_DespatchDocumentReference = etree.SubElement(notaCreditoRoot,"{{{cac}}}DespatchDocumentReference".format(cac=self.namespaces['cac']))
        cbc_ID = etree.SubElement(cac_DespatchDocumentReference,"{{{cbc}}}ID".format(cbc=self.namespaces['cbc']))
        cbc_ID.text = "-" # OPCIONAL - GUIA DE REMISION
        cbc_DocumentTypeCode = etree.SubElement(cac_DespatchDocumentReference,"{{{cbc}}}DocumentTypeCode".format(cbc=self.namespaces['cbc']))
        cbc_DocumentTypeCode.text = "-" # OPCIONAL - CATALOGO 01'''
        #Signature
        cac_Signature = etree.SubElement(notaCreditoRoot, "{{{cac}}}Signature".format(cac=self.namespaces['cac']))
        cbc_Id_Signature = etree.SubElement(cac_Signature,"{{{cbc}}}ID".format(cbc=self.namespaces['cbc']))
        cbc_Id_Signature.text = self.empresa.ruc #RUC DEL EMISOR
        cbc_Note = etree.SubElement(cac_Signature,"{{{cbc}}}Note".format(cbc=self.namespaces['cbc']))
        cbc_Note.text = self.empresa.nombre_comercial  # NOMBRE EMPRESA
        cac_SignatoreParty = etree.SubElement(cac_Signature, "{{{cac}}}SignatoryParty".format(cac=self.namespaces['cac']))
        cac_SignaturePartyIdentification = etree.SubElement(cac_SignatoreParty,"{{{cac}}}PartyIdentification".format(cac=self.namespaces['cac']))
        cbc_ID_PartyIdentification = etree.SubElement(cac_SignaturePartyIdentification,"{{{cbc}}}ID".format(cbc=self.namespaces['cbc']))
        cbc_ID_PartyIdentification.text = self.empresa.ruc #RUC DEL EMISOR
        cac_PartyNameSignatoreParty = etree.SubElement(cac_SignatoreParty,"{{{cac}}}PartyName".format(cac=self.namespaces['cac']))
        cbc_NamePartyName = etree.SubElement(cac_PartyNameSignatoreParty,"{{{cbc}}}Name".format(cbc=self.namespaces['cbc']))
        cbc_NamePartyName.text = etree.CDATA(self.empresa.nombre) #nombre de mi empresa
        cac_DigitalSignatureAttachment = etree.SubElement(cac_Signature,"{{{cac}}}DigitalSignatureAttachment".format(cac=self.namespaces['cac']))
        cac_ExternalReference = etree.SubElement(cac_DigitalSignatureAttachment, "{{{cac}}}ExternalReference".format(cac=self.namespaces['cac']))
        cbc_URI = etree.SubElement(cac_ExternalReference,"{{{cbc}}}URI".format(cbc=self.namespaces['cbc']))
        cbc_URI.text = f"#{self.empresa.nombre_comercial.replace(' ','')}-SIGN"
        #DATOS DEL EMISOR
        cac_AccountingSupplierParty = etree.SubElement(notaCreditoRoot, "{{{cac}}}AccountingSupplierParty".format(cac=self.namespaces['cac']))
        cac_Party = etree.SubElement(cac_AccountingSupplierParty,"{{{cac}}}Party".format(cac=self.namespaces['cac']))
        cac_PartyIdentification = etree.SubElement(cac_Party,"{{{cac}}}PartyIdentification".format(cac=self.namespaces['cac']))
        cbc_ID = etree.SubElement(cac_PartyIdentification,"{{{cbc}}}ID".format(cbc=self.namespaces['cbc']))
        cbc_ID.set("schemeID","6")
        cbc_ID.text = self.empresa.ruc # RUC DEL EMISOR
        cac_PartyName = etree.SubElement(cac_Party,"{{{cac}}}PartyName".format(cac=self.namespaces['cac']))
        cbc_Name = etree.SubElement(cac_PartyName,"{{{cbc}}}Name".format(cbc=self.namespaces['cbc']))
        cbc_Name.text = etree.CDATA(self.empresa.nombre_comercial) #NOMBRE  DEL EMISOR
        cac_PartyLegalEntity = etree.SubElement(cac_Party,"{{{cac}}}PartyLegalEntity".format(cac=self.namespaces['cac']))
        cbc_RegistrationName = etree.SubElement(cac_PartyLegalEntity,"{{{cbc}}}RegistrationName".format(cbc=self.namespaces['cbc']))
        cbc_RegistrationName.text = etree.CDATA(self.empresa.nombre) #RAZON SOCIAL DEL EMISOR
        cac_RegistrationAddress = etree.SubElement(cac_PartyLegalEntity,"{{{cac}}}RegistrationAddress".format(cac=self.namespaces['cac']))
        cbc_ID = etree.SubElement(cac_RegistrationAddress,"{{{cbc}}}ID".format(cbc=self.namespaces['cbc']))
        cbc_ID.text = self.empresa.ubigeo # ubigeo
        cbc_AddressTypeCode = etree.SubElement(cac_RegistrationAddress,"{{{cbc}}}AddressTypeCode".format(cbc=self.namespaces['cbc']))
        cbc_AddressTypeCode.text = "0000" # en el caso de no poder determinar el lugar de laventa, informar “0000”.
        cbc_CitySubdivisionName = etree.SubElement(cac_RegistrationAddress,"{{{cbc}}}CitySubdivisionName".format(cbc=self.namespaces['cbc']))
        if(self.empresa.urbanizacion):
            cbc_CitySubdivisionName.text = self.empresa.urbanizacion # URBANIZACION
        else: cbc_CitySubdivisionName.text = "-" # URBANIZACION
        cbc_CityName = etree.SubElement(cac_RegistrationAddress,"{{{cbc}}}CityName".format(cbc=self.namespaces['cbc']))
        cbc_CityName.text = self.empresa.provincia # PROVINCIA
        cbc_CountrySubentity = etree.SubElement(cac_RegistrationAddress,"{{{cbc}}}CountrySubentity".format(cbc=self.namespaces['cbc']))
        cbc_CountrySubentity.text= self.empresa.departamento # DEPARTAMENTO
        cbc_District = etree.SubElement(cac_RegistrationAddress,"{{{cbc}}}District".format(cbc=self.namespaces['cbc']))
        cbc_District.text= self.empresa.distrito # DISTRITO
        cac_AddressLine = etree.SubElement(cac_RegistrationAddress,"{{{cac}}}AddressLine".format(cac=self.namespaces['cac']))
        cbc_Line = etree.SubElement(cac_AddressLine,"{{{cbc}}}Line".format(cbc=self.namespaces['cbc']))
        cbc_Line.text = etree.CDATA(self.empresa.direccion) #direccion
        cac_Country = etree.SubElement(cac_RegistrationAddress,"{{{cac}}}Country".format(cac=self.namespaces['cac']))
        cbc_IdentificationCode = etree.SubElement(cac_Country,"{{{cbc}}}IdentificationCode".format(cbc=self.namespaces['cbc']))
        cbc_IdentificationCode.text = "PE"
        #DATOS DEL RECEPTOR
        cac_AccountingCustomerParty = etree.SubElement(notaCreditoRoot, "{{{cac}}}AccountingCustomerParty".format(cac=self.namespaces['cac']))
        cac_Party = etree.SubElement(cac_AccountingCustomerParty,"{{{cac}}}Party".format(cac=self.namespaces['cac']))
        cac_PartyIdentification = etree.SubElement(cac_Party,"{{{cac}}}PartyIdentification".format(cac=self.namespaces['cac']))
        cbc_ID = etree.SubElement(cac_PartyIdentification,"{{{cbc}}}ID".format(cbc=self.namespaces['cbc']))
        if(self.ventas.tipComprobante.codigoSunat == '03'): #si es boleta
            cbc_ID.set("schemeID","1") # DNI
        else: cbc_ID.set("schemeID","6") # RUC. catalogo 06
        cbc_ID.text = str(self.ventas.idPedido.cliente_doc) # ruc o DNI del receptor
        cac_PartyLegalEntity = etree.SubElement(cac_Party,"{{{cac}}}PartyLegalEntity".format(cac=self.namespaces['cac']))
        cbc_RegistrationName = etree.SubElement(cac_PartyLegalEntity,"{{{cbc}}}RegistrationName".format(cbc=self.namespaces['cbc']))
        cbc_RegistrationName.text = etree.CDATA(self.ventas.idPedido.cliente) # nombre o razon del cliente
        # FACTURA
        cac_RegistrationAddress = etree.SubElement(cac_PartyLegalEntity,"{{{cac}}}RegistrationAddress".format(cac=self.namespaces['cac']))
        cac_AddressLine = etree.SubElement(cac_RegistrationAddress,"{{{cac}}}AddressLine".format(cac=self.namespaces['cac']))
        cbc_Line = etree.SubElement(cac_AddressLine,"{{{cbc}}}Line".format(cbc=self.namespaces['cbc']))
        cbc_Line.text = etree.CDATA(self.ventas.idPedido.cliente_dir)
        cac_Country = etree.SubElement(cac_RegistrationAddress,"{{{cac}}}Country".format(cac=self.namespaces['cac']))
        cbc_IdentificationCode = etree.SubElement(cac_Country,"{{{cbc}}}IdentificationCode".format(cbc=self.namespaces['cbc']))
        cbc_IdentificationCode.text = "PE"
        #TAXTOTAL
        cac_TaxTotal = etree.SubElement(notaCreditoRoot,"{{{cac}}}TaxTotal".format(cac=self.namespaces['cac']))
        cbc_TaxAmount = etree.SubElement(cac_TaxTotal,"{{{cbc}}}TaxAmount".format(cbc=self.namespaces['cbc']))
        cbc_TaxAmount.set("currencyID","PEN")
        cbc_TaxAmount.text = str(self.notaCredtio.igv) #Total impuestos
        cac_TaxSubtotal = etree.SubElement(cac_TaxTotal,"{{{cac}}}TaxSubtotal".format(cac=self.namespaces['cac']))
        cbc_TaxableAmount = etree.SubElement(cac_TaxSubtotal,"{{{cbc}}}TaxableAmount".format(cbc=self.namespaces['cbc']))
        cbc_TaxableAmount.set("currencyID","PEN")
        cbc_TaxableAmount.text = str(self.notaCredtio.subtotal) #Sum. valor venta (gravadas) subtotal
        cbc_TaxAmount = etree.SubElement(cac_TaxSubtotal,"{{{cbc}}}TaxAmount".format(cbc=self.namespaces['cbc']))
        cbc_TaxAmount.set("currencyID","PEN")
        cbc_TaxAmount.text = str(self.notaCredtio.igv) #impuestos
        cac_TaxCategory = etree.SubElement(cac_TaxSubtotal,"{{{cac}}}TaxCategory".format(cac=self.namespaces['cac']))
        cac_TaxScheme = etree.SubElement(cac_TaxCategory,"{{{cac}}}TaxScheme".format(cac=self.namespaces['cac']))
        cbc_ID = etree.SubElement(cac_TaxScheme,"{{{cbc}}}ID".format(cbc=self.namespaces['cbc']))
        ### CON/SIN IGV.  Catálogo 05
        if (self.ventas.idPedido.igv_total > 0): # CON IGV
            codigo_tributo = '1000'
            nombre_tributo = 'IGV'
            igv = Decimal(str(self.impuesto.valor_porcentaje/100)) # %
            afectacion_igv = '10' #catalogo 07
            print(igv)
        else:   # Sin IGV
            codigo_tributo = '9997'
            nombre_tributo = 'EXO'
            igv = 0
            afectacion_igv = '20' #catalogo 07

        cbc_ID.text = codigo_tributo # Tipo de tributo: 1000 (IGV Impuesto General a las Ventas - Catálogo 05)
        cbc_Name = etree.SubElement(cac_TaxScheme,"{{{cbc}}}Name".format(cbc=self.namespaces['cbc']))
        cbc_Name.text = nombre_tributo
        cbc_TaxTypeCode = etree.SubElement(cac_TaxScheme,"{{{cbc}}}TaxTypeCode".format(cbc=self.namespaces['cbc']))
        cbc_TaxTypeCode.text = "VAT"
        #LegalMonetaryTotal - Total valor venta
        cac_LegalMonetaryTotal = etree.SubElement(notaCreditoRoot,"{{{cac}}}LegalMonetaryTotal".format(cac=self.namespaces['cac']))
        cbc_PayableAmount = etree.SubElement(cac_LegalMonetaryTotal,"{{{cbc}}}PayableAmount".format(cbc=self.namespaces['cbc']))
        cbc_PayableAmount.set("currencyID","PEN")
        cbc_PayableAmount.text = str(self.notaCredtio.subtotal + self.notaCredtio.igv) #Importe total de la venta

        for i in range(len(self.detalle_pedido)):
            #DETALLES
            cac_CreditNoteLine = etree.SubElement(notaCreditoRoot,"{{{cac}}}CreditNoteLine".format(cac=self.namespaces['cac']))
            cbc_ID = etree.SubElement(cac_CreditNoteLine,"{{{cbc}}}ID".format(cbc=self.namespaces['cbc']))
            cbc_ID.text = str(i+1) #Número de orden del detalle
            cbc_CreditedQuantity = etree.SubElement(cac_CreditNoteLine,"{{{cbc}}}CreditedQuantity".format(cbc=self.namespaces['cbc']))
            cbc_CreditedQuantity.set("unitCode","NIU") # Unidad de medida: @unitCode = NIU (Unidad - Catálogo 03)
            cbc_CreditedQuantity.text = str(self.detalle_pedido[i].cantidad) # Cantidad de unidades de venta
            cbc_LineExtensionAmount = etree.SubElement(cac_CreditNoteLine,"{{{cbc}}}LineExtensionAmount".format(cbc=self.namespaces['cbc']))
            cbc_LineExtensionAmount.set("currencyID","PEN")
            cbc_LineExtensionAmount.text = str(self.detalle_pedido[i].importe) #Valor de venta. subtotal 
            cac_PricingReference = etree.SubElement(cac_CreditNoteLine,"{{{cac}}}PricingReference".format(cac=self.namespaces['cac']))
            cac_AlternativeConditionPrice = etree.SubElement(cac_PricingReference,"{{{cac}}}AlternativeConditionPrice".format(cac=self.namespaces['cac']))
            cbc_PriceAmount = etree.SubElement(cac_AlternativeConditionPrice,"{{{cbc}}}PriceAmount".format(cbc=self.namespaces['cbc']))
            cbc_PriceAmount.set("currencyID","PEN")
            cbc_PriceAmount.text = str(round( (self.detalle_pedido[i].precio + (self.detalle_pedido[i].precio * igv) ), 2)) #Precio venta unitario + IGV, round a 2 decimales
            cbc_PriceTypeCode = etree.SubElement(cac_AlternativeConditionPrice,"{{{cbc}}}PriceTypeCode".format(cbc=self.namespaces['cbc']))
            cbc_PriceTypeCode.text = "01" #Tipo de precio: 01 (Precio unitario con IGV - Catálogo 16)
            cac_TaxTotal = etree.SubElement(cac_CreditNoteLine,"{{{cac}}}TaxTotal".format(cac=self.namespaces['cac']))
            cbc_TaxAmount = etree.SubElement(cac_TaxTotal,"{{{cbc}}}TaxAmount".format(cbc=self.namespaces['cbc']))
            cbc_TaxAmount.set("currencyID","PEN")
            cbc_TaxAmount.text = str(round(self.detalle_pedido[i].importe * igv,2)) #Total impuesto detalle round a 2 decimales
            cac_TaxSubtotal = etree.SubElement(cac_TaxTotal,"{{{cac}}}TaxSubtotal".format(cac=self.namespaces['cac']))
            cbc_TaxableAmount = etree.SubElement(cac_TaxSubtotal,"{{{cbc}}}TaxableAmount".format(cbc=self.namespaces['cbc']))
            cbc_TaxableAmount.set("currencyID","PEN")
            cbc_TaxableAmount.text = str(self.detalle_pedido[i].importe) #Valor base para calcular el igv detalle
            cbc_TaxAmount = etree.SubElement(cac_TaxSubtotal,"{{{cbc}}}TaxAmount".format(cbc=self.namespaces['cbc']))
            cbc_TaxAmount.set("currencyID","PEN")
            cbc_TaxAmount.text = str(round(self.detalle_pedido[i].importe * igv,2)) #IGV
            cac_TaxCategory = etree.SubElement(cac_TaxSubtotal,"{{{cac}}}TaxCategory".format(cac=self.namespaces['cac']))
            cbc_Percent = etree.SubElement(cac_TaxCategory,"{{{cbc}}}Percent".format(cbc=self.namespaces['cbc']))
            cbc_Percent.text = str(igv * 100) #Tasa de IGV: 18%
            cbc_TaxExemptionReasonCode = etree.SubElement(cac_TaxCategory,"{{{cbc}}}TaxExemptionReasonCode".format(cbc=self.namespaces['cbc']))
            cbc_TaxExemptionReasonCode.text = afectacion_igv #Tipo de Afectacion IGV: 10, 20 (Gravado, Operación Onerosa - Catálogo 07)
            cac_TaxScheme = etree.SubElement(cac_TaxCategory,"{{{cac}}}TaxScheme".format(cac=self.namespaces['cac']))
            cbc_ID = etree.SubElement(cac_TaxScheme,"{{{cbc}}}ID".format(cbc=self.namespaces['cbc']))
            cbc_ID.text = codigo_tributo # 1000, 9997
            cbc_Name = etree.SubElement(cac_TaxScheme,"{{{cbc}}}Name".format(cbc=self.namespaces['cbc']))
            cbc_Name.text = nombre_tributo # IGV, EXO
            cbc_TaxTypeCode = etree.SubElement(cac_TaxScheme,"{{{cbc}}}TaxTypeCode".format(cbc=self.namespaces['cbc']))
            cbc_TaxTypeCode.text = "VAT"
            #Descripción del producto/servicio
            cac_Item = etree.SubElement(cac_CreditNoteLine,"{{{cac}}}Item".format(cac=self.namespaces['cac']))
            cbc_Description = etree.SubElement(cac_Item,"{{{cbc}}}Description".format(cbc=self.namespaces['cbc']))
            cbc_Description.text = etree.CDATA(str(self.detalle_pedido[i].producto))
            cac_SellersItemIdentification = etree.SubElement(cac_Item,"{{{cac}}}SellersItemIdentification".format(cac=self.namespaces['cac']))
            cbc_ID = etree.SubElement(cac_SellersItemIdentification,"{{{cbc}}}ID".format(cbc=self.namespaces['cbc']))
            cbc_ID.text = str(self.detalle_pedido[i].idAlmacen.idProducto.codigo) # codigo del producto
            #Price
            cac_Price = etree.SubElement(cac_CreditNoteLine,"{{{cac}}}Price".format(cac=self.namespaces['cac']))
            cbc_PriceAmount = etree.SubElement(cac_Price,"{{{cbc}}}PriceAmount".format(cbc=self.namespaces['cbc']))
            cbc_PriceAmount.set("currencyID","PEN")
            cbc_PriceAmount.text = str(self.detalle_pedido[i].precio) #Valor venta unitario

        # Ruta donde deseas guardar el archivo identado
        output_xml_path = 'comprobantes/xml/notaCredito.xml'

        # Guardar el XML identado en otro archivo
        xml_content = etree.tostring(
            notaCreditoRoot,
            xml_declaration=True,
            encoding='utf-8',
            pretty_print=True
        ).decode('utf-8')

        # Eliminar el espacio adicional al final del XML
        xml_content = xml_content.strip()

        # Guardar el XML identado en otro archivo
        with open(output_xml_path, 'w', encoding='utf-8') as output_file:
            output_file.write(xml_content)
        
        with open('comprobantes/xml/notaCredito.xml', 'r', encoding='utf-8') as input_file: # Abrir el archivo original y leer su contenido
           xml_content = input_file.read()

        # Realizar el reemplazo de la etiqueta
        xml_content_modificado = xml_content.replace('<ext:ExtensionContent/>', '<ext:ExtensionContent>\n      </ext:ExtensionContent>')

        with open('comprobantes/xml/notaCredito.xml', 'w', encoding='utf-8') as output_file: # Guardar el archivo modificado en otro archivo
          output_file.write(xml_content_modificado) 
        
        return notaCreditoRoot
    
    def generateComunicBaja(self):
        namespaces = {
            None: "urn:sunat:names:specification:ubl:peru:schema:xsd:VoidedDocuments-1",
            'ext': "urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2",
            'cbc': "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
            'cac': "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
            'ds': "http://www.w3.org/2000/09/xmldsig#",
            'sac': "urn:sunat:names:specification:ubl:peru:schema:xsd:SunatAggregateComponents-1"
        }

        voidedDocuments = etree.Element(
            "VoidedDocuments",
            nsmap=namespaces       
        )
        
        etree.register_namespace('ds', 'http://www.w3.org/2000/09/xmldsig#')
         # UBLExtensions
        ubl_extensions = etree.SubElement(voidedDocuments, "{{{ext}}}UBLExtensions".format(ext=namespaces['ext']))
        ubl_extension = etree.SubElement(ubl_extensions, "{{{ext}}}UBLExtension".format(ext=namespaces['ext']))
        extension_content = etree.SubElement(ubl_extension, "{{{ext}}}ExtensionContent".format(ext=namespaces['ext']))
        # UBLVersionID
        cbc_UBLVersionID = etree.SubElement(voidedDocuments, "{{{cbc}}}UBLVersionID".format(cbc=namespaces['cbc']))
        cbc_UBLVersionID.text = "2.0"
        # CustomizationID
        cbc_CustomizationID = etree.SubElement(voidedDocuments, "{{{cbc}}}CustomizationID".format(cbc=namespaces['cbc']))
        cbc_CustomizationID.text = "1.0"
        # ID
        cbc_ID = etree.SubElement(voidedDocuments, "{{{cbc}}}ID".format(cbc=namespaces['cbc']))
        cbc_ID.text = "RA-20201129-1" #self.ventas.serie+'-'+self.ventas.numComprobante  # "B001-1" Numero de BOLETA
        #ReferenceDate
        cbc_ReferenceDate = etree.SubElement(voidedDocuments, "{{{cbc}}}ReferenceDate".format(cbc=namespaces['cbc']))
        cbc_ReferenceDate.text = "2020-11-26" # str(self.ventas.fecha) # 2020-07-21 fecha de boleta
        cbc_IssueDate = etree.SubElement(voidedDocuments, "{{{cbc}}}IssueDate".format(cbc=namespaces['cbc']))
        cbc_IssueDate.text = "2020-11-29"
        #Signature
        cac_Signature = etree.SubElement(voidedDocuments, "{{{cac}}}Signature".format(cac=namespaces['cac']))
        cbc_Id_Signature = etree.SubElement(cac_Signature,"{{{cbc}}}ID".format(cbc=namespaces['cbc']))
        cbc_Id_Signature.text = self.empresa.ruc #RUC DEL EMISOR
        cac_SignatoreParty = etree.SubElement(cac_Signature, "{{{cac}}}SignatoryParty".format(cac=namespaces['cac']))
        cac_SignaturePartyIdentification = etree.SubElement(cac_SignatoreParty,"{{{cac}}}PartyIdentification".format(cac=namespaces['cac']))
        cbc_ID_PartyIdentification = etree.SubElement(cac_SignaturePartyIdentification,"{{{cbc}}}ID".format(cbc=namespaces['cbc']))
        cbc_ID_PartyIdentification.text = self.empresa.ruc #RUC DEL EMISOR
        cac_PartyNameSignatoreParty = etree.SubElement(cac_SignatoreParty,"{{{cac}}}PartyName".format(cac=namespaces['cac']))
        cbc_NamePartyName = etree.SubElement(cac_PartyNameSignatoreParty,"{{{cbc}}}Name".format(cbc=namespaces['cbc']))
        cbc_NamePartyName.text = etree.CDATA(self.empresa.nombre) #nombre de mi empresa
        cac_DigitalSignatureAttachment = etree.SubElement(cac_Signature,"{{{cac}}}DigitalSignatureAttachment".format(cac=namespaces['cac']))
        cac_ExternalReference = etree.SubElement(cac_DigitalSignatureAttachment, "{{{cac}}}ExternalReference".format(cac=namespaces['cac']))
        cbc_URI = etree.SubElement(cac_ExternalReference,"{{{cbc}}}URI".format(cbc=namespaces['cbc']))
        cbc_URI.text = f"#{self.empresa.nombre_comercial.replace(' ','')}-SIGN"
        #DATOS DEL EMISOR
        cac_AccountingSupplierParty = etree.SubElement(voidedDocuments, "{{{cac}}}AccountingSupplierParty".format(cac=namespaces['cac']))
        cbc_CustomerAssignedAccountID = etree.SubElement(cac_AccountingSupplierParty,"{{{cbc}}}CustomerAssignedAccountID".format(cbc=namespaces['cbc']))
        cbc_CustomerAssignedAccountID.text = self.empresa.ruc # RUC DEL EMISOR
        cbc_AdditionalAccountID = etree.SubElement(cac_AccountingSupplierParty,"{{{cbc}}}AdditionalAccountID".format(cbc=namespaces['cbc']))
        cbc_AdditionalAccountID.text = "6"
        cac_Party = etree.SubElement(cac_AccountingSupplierParty,"{{{cac}}}Party".format(cac=namespaces['cac']))
        cac_PartyLegalEntity = etree.SubElement(cac_Party,"{{{cac}}}PartyLegalEntity".format(cac=namespaces['cac']))
        cbc_RegistrationName = etree.SubElement(cac_PartyLegalEntity,"{{{cbc}}}RegistrationName".format(cbc=namespaces['cbc']))
        cbc_RegistrationName.text = etree.CDATA(self.empresa.nombre) #RAZON SOCIAL DEL EMISOR
        #detalles
        for i in len(self.detalle_anulado):
            sac_VoidedDocumentsLine = etree.SubElement(voidedDocuments,"{{{sac}}}VoidedDocumentsLine".format(sac=namespaces['sac']))
            cbc_LineID = etree.SubElement(sac_VoidedDocumentsLine,"{{{cbc}}}LineID".format(cbc=namespaces['cbc']))
            cbc_LineID.text = str(i+1)
            cbc_DocumentTypeCode = etree.SubElement(sac_VoidedDocumentsLine,"{{{cbc}}}DocumentTypeCode".format(cbc=namespaces['cbc']))
            cbc_DocumentTypeCode.text = "01" # FACTURA
            sac_DocumentSerialID = etree.SubElement(sac_VoidedDocumentsLine,"{{{sac}}}DocumentSerialID".format(sac=namespaces['sac']))
            sac_DocumentSerialID.text = "F001"
            sac_DocumentNumberID = etree.SubElement(sac_VoidedDocumentsLine,"{{{sac}}}DocumentNumberID".format(sac=namespaces['sac']))
            sac_DocumentNumberID.text = "2134" #numero de factura
            sac_VoidReasonDescription = etree.SubElement(sac_VoidedDocumentsLine,"{{{sac}}}VoidReasonDescription".format(sac=namespaces['sac']))
            sac_VoidReasonDescription.text = etree.CDATA("ERROR DE RUC")
        
        # Ruta donde deseas guardar el archivo identado
        output_xml_path = 'comprobantes/xml/comunicBaja.xml'

        # Guardar el XML identado en otro archivo
        xml_content = etree.tostring(
            voidedDocuments,
            xml_declaration=True,
            encoding='utf-8',
            pretty_print=True
        ).decode('utf-8')

        # Eliminar el espacio adicional al final del XML
        xml_content = xml_content.strip()

        # Guardar el XML identado en otro archivo
        with open(output_xml_path, 'w', encoding='utf-8') as output_file:
            output_file.write(xml_content)
        
        with open('comprobantes/xml/comunicBaja.xml', 'r', encoding='utf-8') as input_file: # Abrir el archivo original y leer su contenido
           xml_content = input_file.read()

        # Realizar el reemplazo de la etiqueta
        xml_content_modificado = xml_content.replace('<ext:ExtensionContent/>', '<ext:ExtensionContent>\n      </ext:ExtensionContent>')

        with open('comprobantes/xml/comunicBaja.xml', 'w', encoding='utf-8') as output_file: # Guardar el archivo modificado en otro archivo
          output_file.write(xml_content_modificado) 
        
        return voidedDocuments