from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'countProveedores',views.countProveedoresviewSet,basename='countProveedores')
router.register(r'countProductos',views.countProductoviewSet,basename='countProductos')
router.register(r'countCategorias',views.countCategoriaviewSet,basename='countCategorias')
router.register(r'sumaVentas',views.sumaVentasViewset,basename='sumaVentas')
router.register(r'sumaCompras',views.sumaComprasViewset,basename='sumaCompras')
router.register(r'countSucursal',views.countSucursalviewSet,basename='countSucursal')
router.register(r'ventasxMes',views.ventaxMesViewsets,basename='ventasxMes')

urlpatterns = [
    path('comprobante/<int:idVenta>/<int:idprint>',views.imprimirComprobante, name='comprobante'),
    path('almacenexcel/<int:idcategoria>',views.export_to_excel, name='almacenexcel'),
    path('reporteventas/<str:fini>/<str:ffin>',views.excelReporteVentas, name='reporteventas'),
    path('', include(router.urls))
]
