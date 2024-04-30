# Generated by Django 4.2.3 on 2023-10-29 05:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categorias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=100, unique=True)),
                ('descripcion', models.TextField(blank=True)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Proveedores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empresa', models.CharField(blank=True, max_length=100)),
                ('ruc', models.CharField(blank=True, max_length=30)),
                ('direccion', models.CharField(blank=True, max_length=80)),
                ('correo', models.CharField(blank=True, max_length=30)),
                ('telefono', models.CharField(blank=True, max_length=12)),
                ('celular', models.CharField(blank=True, max_length=12)),
                ('contacto', models.CharField(blank=True, max_length=100)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='UnidadMedida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=20)),
                ('nombrecorto', models.CharField(blank=True, max_length=12)),
                ('proporcion', models.IntegerField(blank=True, null=True)),
                ('unidadStock', models.CharField(blank=True, max_length=10)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Productos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=150, unique=True)),
                ('descripcion', models.TextField(blank=True)),
                ('modelo', models.CharField(blank=True, max_length=100)),
                ('codigo', models.CharField(blank=True, max_length=8, null=True, unique=True)),
                ('activo', models.BooleanField(default=True)),
                ('categoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mantenedoresApp.categorias')),
                ('unidadMedida', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mantenedoresApp.unidadmedida')),
            ],
        ),
    ]