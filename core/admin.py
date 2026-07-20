from django.contrib import admin
from .models import Rol, Usuario, Servicio, Curso, Blog, Matricula


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "descripcion")
    search_fields = ("nombre", "descripcion")
    ordering = ("nombre",)


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "nombres", "apellidos", "correo", "rol", "estado",
                    # "primer_login"
                    )
    list_filter = ("estado", "rol", #"primer_login"
                   )
    search_fields = ("usuario", "nombres", "apellidos", "correo", "telefono")
    ordering = ("apellidos", "nombres")


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "descripcion")
    search_fields = ("nombre", "descripcion")
    ordering = ("nombre",)


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre_curso", "servicio", "costo")
    list_filter = ("servicio",)
    search_fields = ("nombre_curso", "descripcion")
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
