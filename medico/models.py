from django.db import models
from django.contrib.auth.models import User


class Medico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cedula_profesional = models.CharField(max_length=20, unique=True)
    especialidad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.especialidad}"


class Paciente(models.Model):
    medico = models.ForeignKey(
        Medico,
        on_delete=models.CASCADE,
        related_name="pacientes"
    )
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(
        max_length=1,
        choices=[('M', 'Masculino'), ('F', 'Femenino')]
    )

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"



class ExpedienteClinico(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(
        Medico,
        on_delete=models.CASCADE,
        related_name="expedientes"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    antecedentes = models.TextField()

    def __str__(self):
        return f"Expediente de {self.paciente}"


class Diagnostico(models.Model):
    expediente = models.ForeignKey(
        ExpedienteClinico,
        on_delete=models.CASCADE,
        related_name="diagnosticos"
    )
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Diagnóstico {self.fecha.date()}"


class Receta(models.Model):
    diagnostico = models.ForeignKey(
        Diagnostico,
        on_delete=models.CASCADE,
        related_name="recetas"
    )
    medicamento = models.CharField(max_length=200)
    indicaciones = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receta - {self.medicamento}"


class Cita(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    motivo = models.CharField(max_length=200)

    def __str__(self):
        return f"Cita {self.fecha} - {self.paciente}"
# Create your models here.
