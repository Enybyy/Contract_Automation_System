# generator/urls.py

from django.urls import path
from . import views

app_name = 'generator'

urlpatterns = [
    # Ruta existente para plantillas Word
    path('plantillas/', views.gestion_plantillas, name='gestion_plantillas'),

    # ¡NUEVA RUTA! para fuentes de datos Excel
    path('fuentes-datos/', views.gestion_fuentes_datos, name='gestion_fuentes_datos'),
]