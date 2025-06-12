# generator/models.py

from django.db import models
from django.conf import settings  # Para referenciar al modelo de Usuario

# Este modelo representará cada plantilla .docx que un usuario suba.
class PlantillaContrato(models.Model):
    """
    Almacena una plantilla de contrato en formato .docx.
    """
    # Relación con el usuario que subió la plantilla.
    # Si un usuario se elimina, todas sus plantillas también se eliminan (CASCADE).
    propietario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Un nombre descriptivo para que el usuario identifique su plantilla.
    nombre = models.CharField(max_length=255, help_text="Ej: Contrato de Locación de Servicios")
    
    # El archivo .docx en sí. Se guardará en una carpeta 'plantillas/' dentro de tu directorio de medios.
    archivo = models.FileField(upload_to='plantillas/')
    
    # Campo para guardar los placeholders/etiquetas que se extraigan de la plantilla.
    # JSONField es perfecto para guardar una lista de strings. Ej: ["NOMBRE_COMPLETO", "DNI", "FECHA_INICIO"]
    placeholders = models.JSONField(default=list, blank=True, help_text="Las etiquetas extraídas del documento Word.")
    
    # Fecha y hora en que se creó el registro. Se establece automáticamente.
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Esto define cómo se mostrará el objeto en el panel de administración de Django.
        return self.nombre

# Este modelo representará cada archivo Excel que un usuario suba.
class FuenteDeDatos(models.Model):
    """
    Almacena una fuente de datos (archivo Excel) para rellenar los contratos.
    """
    propietario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    nombre = models.CharField(max_length=255, help_text="Ej: Base de Datos Personal Enero 2024")
    
    # El archivo .xlsx. Se guardará en una carpeta 'fuentes_datos/'.
    archivo = models.FileField(upload_to='fuentes_datos/')
    
    # Campo para guardar los nombres de las columnas que se extraigan del Excel.
    # JSONField es ideal aquí también. Ej: ["Nombres y Apellidos", "Documento", "Direccion"]
    columnas = models.JSONField(default=list, blank=True, help_text="Los encabezados de columna extraídos del archivo Excel.")

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre