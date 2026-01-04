from django.urls import path
from . import views

urlpatterns = [
    path("", views.redirect_login, name="home"),
    path("login/", views.login_medico, name="login"),
    path("logout/", views.logout_medico, name="logout"),
    path("panel/", views.panel_medico, name="panel_medico"),

    path("pacientes/", views.lista_pacientes, name="lista_pacientes"),
    path("pacientes/<int:paciente_id>/", views.detalle_paciente, name="detalle_paciente"),
    path("pacientes/nuevo/", views.crear_paciente, name="crear_paciente"),
    path("expediente/<int:expediente_id>/diagnostico/", views.crear_diagnostico, name="crear_diagnostico"),
    path("paciente/<int:paciente_id>/cita/", views.crear_cita, name="crear_cita"),
    path("diagnostico/<int:diagnostico_id>/receta/",views.crear_receta, name="crear_receta"),
    path( "diagnostico/<int:diagnostico_id>/borrar/", views.borrar_diagnostico, name="borrar_diagnostico"),
    path( "diagnostico/<int:diagnostico_id>/editar/", views.editar_diagnostico, name="editar_diagnostico"),
    path("receta/<int:receta_id>/pdf/",views.receta_pdf,name="receta_pdf"),

]



