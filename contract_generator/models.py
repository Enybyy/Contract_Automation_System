# contract_generator/models.py

from django.db import models
from django.contrib.auth.models import User # Importamos el modelo de usuario de Django

# Modelo para almacenar las plantillas de Word (.docx) que sube el usuario
class DocumentTemplate(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name="Nombre de la Plantilla")
    file = models.FileField(upload_to='templates/', verbose_name="Archivo de Plantilla")
    placeholders = models.JSONField(blank=True, null=True, verbose_name="Campos Detectados")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Subida")

    def __str__(self):
        return self.name

# Modelo para almacenar las bases de datos (.xlsx) que sube el usuario
class DataSource(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name="Nombre de la Base de Datos")
    file = models.FileField(upload_to='datasources/', verbose_name="Archivo de Datos")
    headers = models.JSONField(blank=True, null=True, verbose_name="Columnas Detectadas")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Subida")

    def __str__(self):
        return self.name

# Modelo para un "Proyecto de Mapeo", que une una plantilla con una base de datos
class MappingProject(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name="Nombre del Proyecto")
    template = models.ForeignKey(DocumentTemplate, on_delete=models.CASCADE, verbose_name="Plantilla Usada")
    data_source = models.ForeignKey(DataSource, on_delete=models.CASCADE, verbose_name="Base de Datos Usada")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    def __str__(self):
        return self.name

# Modelo que guarda cada mapeo individual (Campo del Word -> Columna del Excel)
class FieldMapping(models.Model):
    project = models.ForeignKey(MappingProject, on_delete=models.CASCADE, related_name="mappings")
    template_placeholder = models.CharField(max_length=255, verbose_name="Campo en Plantilla")
    data_header = models.CharField(max_length=255, verbose_name="Columna en Datos")

    def __str__(self):
        return f'{self.template_placeholder} -> {self.data_header}'