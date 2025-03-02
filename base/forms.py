from django import forms
from .models import Factura

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['kwh', 'valor', 'mes', 'año']  # Incluir los campos mes y año