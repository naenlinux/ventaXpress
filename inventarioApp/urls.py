from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'compras',views.ComprasViewSet)
router.register(r'almacen',views.AlmacenViewSet)
router.register(r'detalle',views.DetalleCompraViewSet)
router.register(r'almacenprecio',views.AlmacenPrecioUMViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/',views.dashboard, name='dashboard')
]