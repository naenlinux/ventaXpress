import base64
import subprocess
from lxml import etree

class FirmaDigital:
    def __init__(self,nombre_xml):
        self.nombre_xml = nombre_xml
        # CARGAMOS LOS CERTIFICADOS PATH
        self.private_key_path =  'config/private.key' 
        self.certificate_path = 'config/certificate.cer'

    def firmar_xml(self):
        valor_resumen = self.calcular_valor_resumen()
        #print (f"valor resumen: {valor_resumen}")
               
        signed_info_content = f"""<ds:SignedInfo xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2" xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:ext="urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2">
  <ds:CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"></ds:CanonicalizationMethod>
  <ds:SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"></ds:SignatureMethod>
  <ds:Reference URI="">
    <ds:Transforms>
      <ds:Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"></ds:Transform>
    </ds:Transforms>
    <ds:DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"></ds:DigestMethod>
    <ds:DigestValue>{valor_resumen}</ds:DigestValue>
  </ds:Reference>
</ds:SignedInfo>"""   

        # Guardar el XML SignedInfo formateado en un archivo
        with open('comprobantes/xml/'+self.nombre_xml+'_signed-info.xml', 'w', newline='\n', encoding='utf-8') as output_file:
            output_file.write(signed_info_content)

        # Comando de OpenSSL para firmar con SHA-1 y RSA - FIRMAR XML
        openssl_command = ['openssl', 'dgst', '-sha1', '-sign', self.private_key_path, 'comprobantes/xml/'+self.nombre_xml+'_signed-info.xml']
        process = subprocess.Popen(openssl_command, stdout=subprocess.PIPE)
        output, _ = process.communicate()
        
        # Convierte la firma binaria a base64 si es necesario
        firma_base64 = base64.b64encode(output).decode('utf-8')

        #print("Firma en base64:", firma_base64)

        # CARGAMOS EL PUBLIC KEY
        with open(self.certificate_path, 'rb') as cert_file:
            cert_data = cert_file.read()
        
        # Eliminar los comentarios del certificado
        cert_data = cert_data.replace(b'-----BEGIN CERTIFICATE-----', b'')
        cert_data = cert_data.replace(b'-----END CERTIFICATE-----', b'')
        
        cert_content = cert_data.decode('utf-8')
        cert_content = cert_content.replace('&#13;', '')
        cert_content = cert_content.replace('\n', '')
        cert_content = cert_content.replace('\r', '')
        # Eliminar los retornos de carro (CR) del certificado

        xml_signature = f"""<ds:Signature Id="FePrimerSign" xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
<ds:SignedInfo xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2" xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:ext="urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2">
  <ds:CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"></ds:CanonicalizationMethod>
  <ds:SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"></ds:SignatureMethod>
  <ds:Reference URI="">
    <ds:Transforms>
      <ds:Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"></ds:Transform>
    </ds:Transforms>
    <ds:DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"></ds:DigestMethod>
    <ds:DigestValue>{valor_resumen}</ds:DigestValue>
  </ds:Reference>
</ds:SignedInfo>
<ds:SignatureValue>{firma_base64}</ds:SignatureValue>
<ds:KeyInfo>
    <ds:X509Data>
        <ds:X509Certificate>{cert_content}</ds:X509Certificate>
    </ds:X509Data>
</ds:KeyInfo>
</ds:Signature>"""

        # INSERTAMOS EL SIGNATURE FIRMADO AL XML PRINCIPAL - COMPROBANTE
        xml_path = 'comprobantes/xml/'+self.nombre_xml+'.xml'
        parser = etree.XMLParser(strip_cdata=False)
        tree = etree.parse(xml_path, parser)
       
        # Busca ExtensionContent para insertar la firma
        extension_content = tree.find('.//ext:ExtensionContent', namespaces={'ext': 'urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2'})

       # Crear un nuevo elemento para signed_info_content y añadirlo a <ext:ExtensionContent>
        signed_info_element = etree.fromstring(xml_signature)
        extension_content.append(signed_info_element)

        # Guarda el XML FIRMADO
        tree.write('comprobantes/xml/'+self.nombre_xml+'_signed.xml', encoding='utf-8', xml_declaration=True)

        #return firma_base64
    
    def calcular_valor_resumen(self):

        with open('comprobantes/xml/'+self.nombre_xml+'.xml', 'rb') as f: # invoice.xml'
            tree = etree.parse(f)

        canonizado = etree.tostring(tree, method='c14n')

        canonizado_sin_comentarios = b'\n'.join([line for line in canonizado.split(b'\n') if not line.strip().startswith(b'<!--')])
        with open('comprobantes/xml/'+self.nombre_xml+'_c14.xml', 'wb') as f:
           f.write(canonizado_sin_comentarios) # guardar el canonico inicial
                
        openssl_command = ['openssl', 'dgst', '-sha1', '-binary', 'comprobantes/xml/'+self.nombre_xml+'_c14.xml'] # obtener el sha1 del archivo canonico
        sha1_hash = subprocess.check_output(openssl_command)
        base64_hash = base64.b64encode(sha1_hash).decode("utf-8") # Convertir el hash a base64
        
        return base64_hash
