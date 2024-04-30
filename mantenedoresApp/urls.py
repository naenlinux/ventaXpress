from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'proveedores', views.ProveedoresViewSet)
router.register(r'categorias', views.CategoriasViewSet)
router.register(r'allcategorias', views.allCategoriasViewSet)
router.register(r'categoriasporname', views.CategoriasViewSetOrderName)
router.register(r'productos', views.ProductosViewSet)
router.register(r'unidadmedida', views.UnidadMedidaViewSet)
router.register(r'unidadmedidall', views.UnidadMedidaViewSetAll)


urlpatterns = [
    path('', include(router.urls)),
]