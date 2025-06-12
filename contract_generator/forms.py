# contract_generator/forms.py

from django import forms
from .models import DocumentTemplate, DataSource

class DocumentTemplateForm(forms.ModelForm):
    class Meta:
        model = DocumentTemplate
        fields = ['name', 'file'] # Solo mostraremos estos campos al usuario
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Contrato de Locación 2024'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Nombre Descriptivo de la Plantilla',
            'file': 'Selecciona tu archivo .docx',
        }


class DataSourceForm(forms.ModelForm):
    class Meta:
        model = DataSource
        fields = ['name', 'file'] # Solo mostraremos estos campos al usuario
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Personal Campaña Junio'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Nombre Descriptivo de la Base de Datos',
            'file': 'Selecciona tu archivo .xlsx',
        }
        
from .models import MappingProject, DocumentTemplate, DataSource

class MappingProjectForm(forms.ModelForm):
    # Sobrescribimos los campos para filtrarlos por el usuario actual
    template = forms.ModelChoiceField(
        queryset=DocumentTemplate.objects.none(),
        label="1. Selecciona una Plantilla",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    data_source = forms.ModelChoiceField(
        queryset=DataSource.objects.none(),
        label="2. Selecciona una Base de Datos",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = MappingProject
        fields = ['name', 'template', 'data_source']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Contratos Campaña Julio'}),
        }
        labels = {
            'name': 'Dale un Nombre a tu Proyecto de Mapeo',
        }

    # El constructor es clave para filtrar los querysets
    def __init__(self, *args, **kwargs):
        # Extraemos el usuario que pasaremos desde la vista
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Filtramos los desplegables para que solo muestren los archivos del usuario logueado
            self.fields['template'].queryset = DocumentTemplate.objects.filter(owner=user)
            self.fields['data_source'].queryset = DataSource.objects.filter(owner=user)
