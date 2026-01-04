from django.db import models

class Especialidad(models.Model):
    id_especialidad = models.AutoField(db_column='ID_Especialidad', primary_key=True)
    nombre = models.CharField(db_column='Nombre', unique=True, max_length=50)
    descripcion = models.CharField(db_column='Descripcion', max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'Especialidad'
        verbose_name_plural = "Especialidades"

    def __str__(self):
        return self.nombre


class Consultorio(models.Model):
    id_consultorio = models.AutoField(db_column='ID_Consultorio', primary_key=True)
    numero = models.CharField(db_column='Numero', unique=True, max_length=10)
    area = models.CharField(db_column='Area', max_length=50)
    turno = models.CharField(db_column='Turno', max_length=20)

    class Meta:
        db_table = 'Consultorio'

    def __str__(self):
        return f"{self.numero} - {self.area}"


class Medicamento(models.Model):
    id_medicamento = models.AutoField(db_column='ID_Medicamento', primary_key=True)
    nombre = models.CharField(db_column='Nombre', max_length=100)
    laboratorio = models.CharField(db_column='Laboratorio', max_length=100)
    principio_activo = models.CharField(db_column='PrincipioActivo', max_length=100)
    gramaje = models.CharField(db_column='Gramaje', max_length=50)
    cantidad_stock = models.IntegerField(db_column='CantidadStock')
    fecha_caducidad = models.DateField(db_column='FechaCaducidad', blank=True, null=True)

    class Meta:
        db_table = 'Medicamento'

    def __str__(self):
        return f"{self.nombre} ({self.gramaje})"


class Medico(models.Model):
    id_medico = models.AutoField(db_column='ID_Medico', primary_key=True)
    nombre_completo = models.CharField(db_column='NombreCompleto', max_length=150)
    cedula_profesional = models.CharField(db_column='CedulaProfesional', unique=True, max_length=20)
    telefono = models.CharField(db_column='Telefono', max_length=15, blank=True, null=True)
    correo_institucional = models.CharField(db_column='CorreoInstitucional', max_length=100, blank=True, null=True)
    especialidad = models.ForeignKey(Especialidad, models.DO_NOTHING, db_column='ID_Especialidad')

    class Meta:
        db_table = 'Medico'

    def __str__(self):
        return f"Dr. {self.nombre_completo}"


class Paciente(models.Model):
    id_paciente = models.AutoField(db_column='ID_Paciente', primary_key=True)
    curp = models.CharField(db_column='CURP', unique=True, max_length=18)
    rfc = models.CharField(db_column='RFC', max_length=13, blank=True, null=True)
    nombre_completo = models.CharField(db_column='NombreCompleto', max_length=150)
    fecha_nacimiento = models.DateField(db_column='FechaNacimiento')
    direccion = models.CharField(db_column='Direccion', max_length=250, blank=True, null=True)
    es_asegurado = models.BooleanField(db_column='EsAsegurado', blank=True, null=True)
    tiene_dependientes = models.BooleanField(db_column='TieneDependientes', blank=True, null=True)

    class Meta:
        db_table = 'Paciente'

    def __str__(self):
        return self.nombre_completo


class TelefonoPaciente(models.Model):
    id_telefono = models.AutoField(db_column='ID_Telefono', primary_key=True)
    paciente = models.ForeignKey(Paciente, models.DO_NOTHING, db_column='ID_Paciente')
    numero = models.CharField(db_column='Numero', max_length=15)
    tipo = models.CharField(db_column='Tipo', max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'TelefonoPaciente'


class Cita(models.Model):
    id_cita = models.AutoField(db_column='ID_Cita', primary_key=True)
    paciente = models.ForeignKey(Paciente, models.DO_NOTHING, db_column='ID_Paciente')
    medico = models.ForeignKey('Medico', models.DO_NOTHING, db_column='ID_Medico')
    consultorio = models.ForeignKey(Consultorio, models.DO_NOTHING, db_column='ID_Consultorio')
    fecha_hora = models.DateTimeField(db_column='FechaHora')
    estado = models.CharField(db_column='Estado', max_length=20, blank=True, null=True)
    pago_realizado = models.BooleanField(db_column='PagoRealizado', blank=True, null=True)

    class Meta:
        db_table = 'Cita'


class Triage(models.Model):
    id_triage = models.AutoField(db_column='ID_Triage', primary_key=True)
    paciente = models.ForeignKey(Paciente, models.DO_NOTHING, db_column='ID_Paciente')
    medico_urgencias = models.ForeignKey(Medico, models.DO_NOTHING, db_column='ID_MedicoUrgencias')
    nivel = models.CharField(db_column='Nivel', max_length=20)
    signos_vitales = models.TextField(db_column='SignosVitales', blank=True, null=True)
    fecha_hora = models.DateTimeField(db_column='FechaHora', blank=True, null=True)

    class Meta:
        db_table = 'Triage'


class Diagnostico(models.Model):
    id_diagnostico = models.AutoField(db_column='ID_Diagnostico', primary_key=True)
    cita = models.OneToOneField(Cita, models.DO_NOTHING, db_column='ID_Cita', blank=True, null=True)
    paciente = models.ForeignKey(Paciente, models.DO_NOTHING, db_column='ID_Paciente')
    medico = models.ForeignKey(Medico, models.DO_NOTHING, db_column='ID_Medico')
    fecha_hora = models.DateTimeField(db_column='FechaHora', blank=True, null=True)
    codigo_cie10 = models.CharField(db_column='CodigoCIE10', max_length=20, blank=True, null=True)
    descripcion_diagnostico = models.TextField(db_column='DescripcionDiagnostico')
    tratamiento = models.TextField(db_column='Tratamiento')
    observaciones = models.TextField(db_column='Observaciones', blank=True, null=True)

    class Meta:
        db_table = 'Diagnostico'


class Receta(models.Model):
    id_receta = models.AutoField(db_column='ID_Receta', primary_key=True)
    diagnostico = models.ForeignKey(Diagnostico, models.DO_NOTHING, db_column='ID_Diagnostico')
    fecha_emision = models.DateTimeField(db_column='FechaEmision', blank=True, null=True)
    firma_digital = models.TextField(db_column='FirmaDigital', blank=True, null=True)

    class Meta:
        db_table = 'Receta'


class DetalleReceta(models.Model):
    id_detalle_receta = models.AutoField(db_column='ID_DetalleReceta', primary_key=True)
    receta = models.ForeignKey(Receta, models.DO_NOTHING, db_column='ID_Receta')
    medicamento = models.ForeignKey(Medicamento, models.DO_NOTHING, db_column='ID_Medicamento')
    dosis = models.CharField(db_column='Dosis', max_length=100)
    duracion = models.CharField(db_column='Duracion', max_length=50)
    cantidad_surtir = models.IntegerField(db_column='CantidadSurtir')

    class Meta:
        db_table = 'DetalleReceta'