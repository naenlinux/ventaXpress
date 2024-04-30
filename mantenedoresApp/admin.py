from django.contrib import admin
from .models import Proveedores, Categorias, Productos

# Register your models here.
admin.site.register(
    [
        Proveedores, Categorias, Productos
    ]
)