# Generated by Django 5.2.3 on 2025-06-12 01:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FuenteDeDatos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(help_text='Ej: Base de Datos Personal Enero 2024', max_length=255)),
                ('archivo', models.FileField(upload_to='fuentes_datos/')),
                ('columnas', models.JSONField(blank=True, default=list, help_text='Los encabezados de columna extraídos del archivo Excel.')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('propietario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PlantillaContrato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(help_text='Ej: Contrato de Locación de Servicios', max_length=255)),
                ('archivo', models.FileField(upload_to='plantillas/')),
                ('placeholders', models.JSONField(blank=True, default=list, help_text='Las etiquetas extraídas del documento Word.')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('propietario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
