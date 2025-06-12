# contract_generator/urls.py

from django.contrib import admin
from django.urls import path, include # Asegúrate de importar 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Cualquier URL que empiece con 'app/' será manejada por nuestra app 'generator'
    path('app/', include('generator.urls')),
]