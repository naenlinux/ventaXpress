from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'empresa',views.EmpresaViewSet)
router.register(r'moneda',views.MonedaViewset)
router.register(r'tipocomprobante',views.TipoComprobantesViewset)
router.register(r'comprobanteconfig',views.ComprobanteConfigViewset)
router.register(r'impuesto',views.ImpuestoViewset)
router.register(r'sucursal',views.SucursalViewset)
router.register(r'usuarios',views.UsuariosViewset)
router.register(r'grupos',views.GruposViewset)
router.register(r'enviarsunat',views.EnviarSunatViewset)

urlpatterns = [
    path('',include(router.urls)),
]

