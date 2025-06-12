# generator/urls.py

from django.urls import path
from . import views

# Este es un buen truco para organizar las URLs de tu app.
app_name = 'generator'

urlpatterns = [
    # La URL para listar y subir plantillas.
    # views.gestion_plantillas es la función que vamos a crear en views.py
    path('plantillas/', views.gestion_plantillas, name='gestion_plantillas'),
]