from django import forms
from .models import Paciente
from .models import Diagnostico
from .models import Cita
from .models import Receta


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ["nombre", "apellidos", "fecha_nacimiento", "sexo"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "apellidos": forms.TextInput(attrs={"class": "form-control"}),
            "fecha_nacimiento": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "sexo": forms.Select(attrs={"class": "form-select"}),
        }



class DiagnosticoForm(forms.ModelForm):
    class Meta:
        model = Diagnostico
        fields = ["descripcion"]
        widgets = {
            "descripcion": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Descripción del diagnóstico"
            }),
        }

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ["fecha", "motivo"]
        widgets = {
            "fecha": forms.DateTimeInput(attrs={
                "class": "form-control",
                "type": "datetime-local"
            }),
            "motivo": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Motivo de la cita"
            }),
        }

class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ["medicamento", "indicaciones"]
        widgets = {
            "medicamento": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nombre del medicamento"
            }),
            "indicaciones": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Indicaciones médicas"
            }),
        }


