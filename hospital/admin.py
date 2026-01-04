from django.contrib import admin
from .models import Especialidad, Medico, Paciente, Cita, Medicamento

# Esto permite ver y editar las tablas desde la web de admin
admin.site.register(Especialidad)
admin.site.register(Medico)
admin.site.register(Paciente)
admin.site.register(Cita)
admin.site.register(Medicamento)