# contract_system/urls.py
from django.contrib import admin
from django.urls import path, include # Asegúrate de que 'include' esté importado
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('contract_generator.urls')), # Incluimos las URLs de nuestra app
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)