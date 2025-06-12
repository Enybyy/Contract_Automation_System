# contract_generator/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    # Nuevas URLs
    path('projects/create/', views.create_mapping_project_view, name='create_project'),
    path('projects/<int:project_id>/map/', views.map_fields_view, name='map_fields'),
]