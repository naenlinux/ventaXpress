from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'caja',views.CajaViewSet)
router.register(r'ventas',views.VentasViewSet)
router.register(r'reporteventas',views.ReporteVentasViewSet)
router.register(r'pedidos',views.PedidosViewSet)
router.register(r'detalle',views.PedidoDetalleViewSet)
router.register(r'notacredito',views.NotaCreditoViewSet)


urlpatterns = [
    path('', include(router.urls)),
]