from django.urls import path, include
from rest_framework import routers
from .views import GenerarXmlNC, NotaCreditoViewset, GenerarXml, EnviarSunatXML

router = routers.DefaultRouter()
router.register(r'codigonotacredito', NotaCreditoViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('generarxml/', GenerarXml.as_view(), name='generarxml'),
    path('enviarsunatxml/', EnviarSunatXML.as_view(), name='enviarsunatxml'),
    path('generarxmlnc/', GenerarXmlNC.as_view(), name='generarxmlnc'),
]