# generator/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required # Para proteger la vista
from .models import PlantillaContrato
import docx # Necesitamos python-docx para leer el archivo
import re

# La función que extrae los placeholders. Podríamos moverla a un archivo utils.py más adelante.
def extraer_placeholders(ruta_archivo_docx):
    """
    Analiza un archivo .docx y extrae todas las etiquetas entre corchetes.
    Ej: [NOMBRE], [DNI] -> ["NOMBRE", "DNI"]
    """
    try:
        documento = docx.Document(ruta_archivo_docx)
        placeholders = set() # Usamos un set para evitar duplicados

        # Expresión regular para encontrar texto entre corchetes
        regex = r"\[(.*?)\]"

        for p in documento.paragraphs:
            encontrados = re.findall(regex, p.text)
            for placeholder in encontrados:
                placeholders.add(placeholder.strip()) # .strip() para quitar espacios
        
        # También buscar en tablas
        for table in documento.tables:
            for row in table.rows:
                for cell in row.cells:
                    for p in cell.paragraphs:
                        encontrados = re.findall(regex, p.text)
                        for placeholder in encontrados:
                            placeholders.add(placeholder.strip())
        
        return list(placeholders)
    except Exception as e:
        print(f"Error al extraer placeholders: {e}")
        return []

@login_required # Esto asegura que solo usuarios logueados puedan acceder
def gestion_plantillas(request):
    # Si el método es POST, significa que el usuario está enviando el formulario
    if request.method == 'POST':
        # Obtenemos los datos del formulario
        nombre_plantilla = request.POST.get('nombre_plantilla')
        archivo_plantilla = request.FILES.get('archivo_plantilla')

        if nombre_plantilla and archivo_plantilla:
            # Creamos una instancia del modelo pero aún no la guardamos en la BD
            nueva_plantilla = PlantillaContrato(
                propietario=request.user,
                nombre=nombre_plantilla,
                archivo=archivo_plantilla
            )
            # Guardamos para que el archivo físico se suba al servidor
            nueva_plantilla.save()

            # Ahora que el archivo está en el servidor, podemos analizarlo
            # El .path nos da la ruta absoluta al archivo
            placeholders_extraidos = extraer_placeholders(nueva_plantilla.archivo.path)
            
            # Guardamos la lista de placeholders en el modelo
            nueva_plantilla.placeholders = placeholders_extraidos
            nueva_plantilla.save() # Guardamos de nuevo para actualizar el campo placeholders

            # Redirigimos a la misma página para ver la plantilla en la lista
            return redirect('generator:gestion_plantillas')

    # Si el método es GET (o si el POST falla), mostramos la página normal
    # Obtenemos todas las plantillas que pertenecen al usuario actual
    plantillas_usuario = PlantillaContrato.objects.filter(propietario=request.user)

    # Creamos el contexto para pasarlo a la plantilla HTML
    context = {
        'plantillas': plantillas_usuario,
    }
    
    # Renderizamos la plantilla HTML con el contexto
    return render(request, 'generator/gestion_plantillas.html', context)