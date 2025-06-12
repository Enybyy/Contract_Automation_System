# generator/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PlantillaContrato
import docx
import re
import os # <-- ¡AQUÍ ESTÁ LA LÍNEA QUE FALTABA!

def extraer_placeholders(ruta_archivo_docx):
    """
    Analiza un archivo .docx y extrae todas las etiquetas entre corchetes.
    """
    try:
        documento = docx.Document(ruta_archivo_docx)
        placeholders = set()
        regex = r"\[(.*?)\]"
        for p in documento.paragraphs:
            encontrados = re.findall(regex, p.text)
            for placeholder in encontrados:
                placeholders.add(placeholder.strip())
        for table in documento.tables:
            for row in table.rows:
                for cell in row.cells:
                    for p in cell.paragraphs:
                        encontrados = re.findall(regex, p.text)
                        for placeholder in encontrados:
                            placeholders.add(placeholder.strip())
        return list(placeholders)
    except Exception as e:
        print(f"Error crítico al analizar el archivo DOCX: {e}")
        return None


@login_required
def gestion_plantillas(request):
    context = {
        'plantillas': PlantillaContrato.objects.filter(propietario=request.user),
        'error': None
    }

    if request.method == 'POST':
        nombre_plantilla = request.POST.get('nombre_plantilla')
        archivo_plantilla = request.FILES.get('archivo_plantilla')

        # 1. Validar que ambos campos están presentes
        if not nombre_plantilla or not archivo_plantilla:
            context['error'] = "Error: Debes proporcionar un nombre y seleccionar un archivo."
            return render(request, 'generator/gestion_plantillas.html', context)

        # 2. Validar la extensión del archivo de forma segura
        nombre_archivo = archivo_plantilla.name
        _ , extension = os.path.splitext(nombre_archivo)

        if extension.lower() != '.docx':
            context['error'] = (
                "Formato de archivo no válido. "
                "Solo se aceptan archivos Word modernos (.docx). "
                "Si tu archivo es .doc, por favor ábrelo en Word y guárdalo como .docx."
            )
            return render(request, 'generator/gestion_plantillas.html', context)

        nueva_plantilla = PlantillaContrato(
            propietario=request.user,
            nombre=nombre_plantilla,
            archivo=archivo_plantilla
        )
        nueva_plantilla.save()

        placeholders_extraidos = extraer_placeholders(nueva_plantilla.archivo.path)
        
        if placeholders_extraidos is None:
            context['error'] = "Error: El archivo .docx parece estar corrupto o no se puede leer."
            # Borramos el registro y el archivo si no se puede procesar
            nueva_plantilla.delete() 
            return render(request, 'generator/gestion_plantillas.html', context)

        nueva_plantilla.placeholders = placeholders_extraidos
        nueva_plantilla.save()
        
        return redirect('generator:gestion_plantillas')

    return render(request, 'generator/gestion_plantillas.html', context)