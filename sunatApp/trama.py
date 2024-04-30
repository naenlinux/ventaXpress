class TramaSOAPGenerator:
    def __init__(self) -> None:
        pass
    def generar_trama_soap(username, password, file_name, zip_b64):
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
