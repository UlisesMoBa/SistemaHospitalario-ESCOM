from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Medico
from .models import Paciente, ExpedienteClinico, Diagnostico, Receta
from .forms import PacienteForm
from .forms import DiagnosticoForm
from .forms import CitaForm
from django.shortcuts import get_object_or_404
from .forms import RecetaForm
from .models import Cita
from django.http import HttpResponse
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

def login_medico(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                # Verificar que el usuario sea médico
                Medico.objects.get(user=user)
                login(request, user)
                return redirect("panel_medico")
            except Medico.DoesNotExist:
                return render(request, "medico/login.html", {
                    "error": "Este usuario no es médico"
                })
        else:
            return render(request, "medico/login.html", {
                "error": "Usuario o contraseña incorrectos"
            })

    return render(request, "medico/login.html")


@login_required
def panel_medico(request):
    medico = Medico.objects.get(user=request.user)
    return render(request, "medico/panel.html", {"medico": medico})


def logout_medico(request):
    logout(request)
    return redirect("login")



def redirect_login(request):
    return redirect("login")



@login_required
def lista_pacientes(request):
    medico = Medico.objects.get(user=request.user)
    pacientes = Paciente.objects.filter(medico=medico)

    return render(request, "medico/pacientes.html", {
        "pacientes": pacientes
    })


@login_required
def detalle_paciente(request, paciente_id):
    medico = Medico.objects.get(user=request.user)

    paciente = get_object_or_404(
        Paciente,
        id=paciente_id,
        medico=medico
    )

    expediente, creado = ExpedienteClinico.objects.get_or_create(
        paciente=paciente,
        defaults={"medico": medico, "antecedentes": ""}
    )

    diagnosticos = Diagnostico.objects.filter(expediente=expediente)

    # 👇 NUEVO: obtener recetas y citas
    recetas = Receta.objects.filter(diagnostico__expediente=expediente)
    citas = Cita.objects.filter(paciente=paciente)

    return render(request, "medico/paciente_detalle.html", {
        "paciente": paciente,
        "expediente": expediente,
        "diagnosticos": diagnosticos,
        "recetas": recetas,
        "citas": citas,
    })




@login_required
def crear_paciente(request):
    medico = Medico.objects.get(user=request.user)

    if request.method == "POST":
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save(commit=False)
            paciente.medico = medico  # 👈 asociación automática
            paciente.save()
            return redirect("lista_pacientes")
    else:
        form = PacienteForm()

    return render(request, "medico/paciente_form.html", {"form": form})

@login_required
def crear_diagnostico(request, expediente_id):
    expediente = ExpedienteClinico.objects.get(id=expediente_id)

    if request.method == "POST":
        form = DiagnosticoForm(request.POST)
        if form.is_valid():
            diagnostico = form.save(commit=False)
            diagnostico.expediente = expediente
            diagnostico.save()

            # 🔴 AQUÍ ESTABA EL ERROR
            return redirect(
                "detalle_paciente",
                paciente_id=expediente.paciente.id
            )
    else:
        form = DiagnosticoForm()

    return render(request, "medico/diagnostico_form.html", {
        "form": form,
        "expediente": expediente
    })


@login_required
def crear_cita(request, paciente_id):
    paciente = Paciente.objects.get(id=paciente_id)
    medico = Medico.objects.get(user=request.user)

    if request.method == "POST":
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.paciente = paciente
            cita.medico = medico
            cita.save()
            return redirect("detalle_paciente", paciente.id)
    else:
        form = CitaForm()

    return render(request, "medico/cita_form.html", {
        "form": form,
        "paciente": paciente
    })

@login_required
def crear_receta(request, diagnostico_id):
    diagnostico = get_object_or_404(Diagnostico, id=diagnostico_id)

    if request.method == "POST":
        form = RecetaForm(request.POST)
        if form.is_valid():
            receta = form.save(commit=False)
            receta.diagnostico = diagnostico
            receta.save()

            # 🔴 REDIRECCIÓN CORRECTA AL PACIENTE
            return redirect(
                "detalle_paciente",
                paciente_id=diagnostico.expediente.paciente.id
            )
    else:
        form = RecetaForm()

    return render(request, "medico/receta_form.html", {
        "form": form,
        "diagnostico": diagnostico
    })

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Diagnostico


@login_required
def borrar_diagnostico(request, diagnostico_id):
    diagnostico = get_object_or_404(Diagnostico, id=diagnostico_id)
    paciente_id = diagnostico.expediente.paciente.id

    if request.method == "POST":
        diagnostico.delete()
        return redirect("detalle_paciente", paciente_id=paciente_id)

    return render(request, "medico/confirmar_borrar_diagnostico.html", {
        "diagnostico": diagnostico
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Diagnostico
from .forms import DiagnosticoForm


@login_required
def editar_diagnostico(request, diagnostico_id):
    diagnostico = get_object_or_404(Diagnostico, id=diagnostico_id)
    paciente_id = diagnostico.expediente.paciente.id

    if request.method == "POST":
        form = DiagnosticoForm(request.POST, instance=diagnostico)
        if form.is_valid():
            form.save()
            return redirect("detalle_paciente", paciente_id=paciente_id)
    else:
        form = DiagnosticoForm(instance=diagnostico)

    return render(request, "medico/diagnostico_form.html", {
        "form": form,
        "expediente": diagnostico.expediente,
        "editar": True
    })


@login_required
def receta_pdf(request, receta_id):
    receta = get_object_or_404(Receta, id=receta_id)

    paciente = receta.diagnostico.expediente.paciente
    medico = receta.diagnostico.expediente.medico
    diagnostico = receta.diagnostico

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="receta_{paciente.id}.pdf"'

    p = canvas.Canvas(response, pagesize=LETTER)
    width, height = LETTER

    y = height - 50

    # Encabezado
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "RECETA MÉDICA")
    y -= 30

    p.setFont("Helvetica", 11)
    p.drawString(50, y, f"Médico: {medico.user.get_full_name()}")
    y -= 20
    p.drawString(50, y, f"Especialidad: {medico.especialidad}")
    y -= 20
    p.drawString(50, y, f"Cédula Profesional: {medico.cedula_profesional}")
    y -= 30

    # Paciente
    p.setFont("Helvetica-Bold", 11)
    p.drawString(50, y, "Paciente:")
    y -= 20

    p.setFont("Helvetica", 11)
    p.drawString(50, y, f"Nombre: {paciente.nombre} {paciente.apellidos}")
    y -= 20
    p.drawString(50, y, f"Fecha de nacimiento: {paciente.fecha_nacimiento}")
    y -= 30

    # Diagnóstico
    p.setFont("Helvetica-Bold", 11)
    p.drawString(50, y, "Diagnóstico:")
    y -= 20

    p.setFont("Helvetica", 11)
    p.drawString(50, y, diagnostico.descripcion)
    y -= 30

    # Receta
    p.setFont("Helvetica-Bold", 11)
    p.drawString(50, y, "Medicamento:")
    y -= 20

    p.setFont("Helvetica", 11)
    p.drawString(50, y, receta.medicamento)
    y -= 30

    p.setFont("Helvetica-Bold", 11)
    p.drawString(50, y, "Indicaciones:")
    y -= 20

    p.setFont("Helvetica", 11)
    text = p.beginText(50, y)
    for linea in receta.indicaciones.split("\n"):
        text.textLine(linea)
    p.drawText(text)

    # Firma
    y -= 80
    p.line(50, y, 250, y)
    y -= 15
    p.drawString(50, y, "Firma del médico")

    p.showPage()
    p.save()

    return response
