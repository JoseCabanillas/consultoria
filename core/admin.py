from django.contrib import admin
from .models import Rol, Usuario, Servicio, Curso, Blog, Matricula, Especialidad, Docente, Nota


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "descripcion")
    search_fields = ("nombre", "descripcion")
    ordering = ("nombre",)


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "nombres", "apellidos", "correo", "rol", "estado")
    list_filter = ("estado", "rol")
    search_fields = ("usuario", "nombres", "apellidos", "correo", "telefono")
    ordering = ("apellidos", "nombres")


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "descripcion")
    search_fields = ("nombre", "descripcion")
    ordering = ("nombre",)


@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ("idEspecialidad", "nomEspecialidad")
    search_fields = ("nomEspecialidad",)
    ordering = ("nomEspecialidad",)


@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display = ("iddocente", "priNombre", "apePaterno", "apeMaterno", "dni", "idEspecialidad")
    list_filter = ("idEspecialidad",)
    search_fields = ("priNombre", "segNombre", "terNombre", "apePaterno", "apeMaterno", "dni")
    ordering = ("apePaterno", "priNombre")


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre_curso", "servicio", "docente", "costo")
    list_filter = ("servicio", "docente")
    search_fields = ("nombre_curso", "descripcion", "docente__priNombre", "docente__apePaterno")
    ordering = ("nombre_curso",)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "usuario", "servicio", "fecha_publicacion")
    list_filter = ("servicio", "fecha_publicacion")
    search_fields = ("titulo", "textoblog")
    date_hierarchy = "fecha_publicacion"


@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "curso", "fecha_matricula", "estado_matricula", "nota_final")
    list_filter = ("estado_matricula", "fecha_matricula")
    search_fields = ("usuario__nombres", "usuario__apellidos", "curso__nombre_curso")
    date_hierarchy = "fecha_matricula"


@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display = ("idnota", "idmatricula", "valor_nota", "fec_crea")
    list_filter = ("fec_crea",)
    search_fields = (
        "idmatricula__usuario__nombres",
        "idmatricula__usuario__apellidos",
        "idmatricula__curso__nombre_curso",
        "valor_nota",
    )
    date_hierarchy = "fec_crea"
