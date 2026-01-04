from django.contrib import admin
from .models import Medico, Paciente, ExpedienteClinico, Diagnostico, Receta


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "especialidad", "cedula_profesional", "telefono")
    search_fields = ("user__username", "user__first_name", "user__last_name", "cedula_profesional")
    list_filter = ("especialidad",)


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "apellidos", "sexo", "fecha_nacimiento")
    search_fields = ("nombre", "apellidos")
    list_filter = ("sexo",)


@admin.register(ExpedienteClinico)
class ExpedienteClinicoAdmin(admin.ModelAdmin):
    list_display = ("id", "paciente", "medico", "fecha_creacion")
    list_filter = ("medico", "fecha_creacion")


@admin.register(Diagnostico)
class DiagnosticoAdmin(admin.ModelAdmin):
    list_display = ("id", "expediente", "fecha")
    list_filter = ("fecha",)


@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    list_display = ("id", "medicamento", "fecha")
    list_filter = ("fecha",)



# Register your models here.
