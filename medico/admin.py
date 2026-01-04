from django.contrib import admin

from django.contrib import admin
from .models import Medico, Paciente, ExpedienteClinico, Diagnostico, Receta

admin.site.register(Medico)
admin.site.register(Paciente)
admin.site.register(ExpedienteClinico)
admin.site.register(Diagnostico)
admin.site.register(Receta)

# Register your models here.
