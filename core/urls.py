from django.urls import path
from .views import (
    usuario_lista, usuario_create, usuario_update, usuario_delete,
    curso_lista, curso_create, curso_update, curso_delete,
    curso_publico_lista,
    rol_lista, rol_create, rol_update, rol_delete,
    ServicioListView, ServicioCreateView, ServicioUpdateView, ServicioDeleteView,
    servicio_publico_lista,
    blog_lista, blog_create, blog_update, blog_delete, blog_detalle,
    blog_publico_lista, BlogDetallePublicoView,
    MatriculaLista, MatriculaCreate, MatriculaDelete, MatriculaUpdate,
    inicio, login_view, CustomLogoutView,
    CursoDetalleView, CursoDetallePublicoView,
    # ✅ CRUD de Notas
    nota_list, nota_create, nota_update, nota_delete,nota_export,
    # ✅ CRUD de Especialidad
    especialidad_lista,especialidad_create,especialidad_update,especialidad_delete,
    # ✅ CRUD de Docente
    docente_lista,docente_create,docente_update,docente_delete
)


urlpatterns = [
    # Página pública (raíz del sitio)
    path("", servicio_publico_lista.as_view(), name="servicio_publico"),

    # Página privada de inicio (después de login)
    path("inicio/", inicio, name="inicio"),

    # BLOGS
    path("blogs/servicio/<int:servicio_id>/", blog_publico_lista.as_view(), name="blogs_por_servicio"),
    path("blogs/publico/<int:pk>/", BlogDetallePublicoView.as_view(), name="blog_detalle_publico"),
    path("blogs/", blog_lista.as_view(), name="blog_lista"),
    path("blogs/nuevo/", blog_create.as_view(), name="blog_create"),
    path("blogs/<int:pk>/editar/", blog_update.as_view(), name="blog_update"),
    path("blogs/<int:pk>/eliminar/", blog_delete.as_view(), name="blog_delete"),
    path("blogs/<int:pk>/", blog_detalle.as_view(), name="blog_detalle"),

    # Login y logout
    path("login/", login_view, name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),

    # SERVICIOS
    path("servicios/", ServicioListView.as_view(), name="servicio_lista"),
    path("servicios/nuevo/", ServicioCreateView.as_view(), name="servicio_create"),
    path("servicios/<int:pk>/editar/", ServicioUpdateView.as_view(), name="servicio_update"),
    path("servicios/<int:pk>/eliminar/", ServicioDeleteView.as_view(), name="servicio_delete"),

    # ROLES
    path("roles/", rol_lista.as_view(), name="rol_lista"),
    path("roles/nuevo/", rol_create.as_view(), name="rol_create"),
    path("roles/<int:pk>/editar/", rol_update.as_view(), name="rol_update"),
    path("roles/<int:pk>/eliminar/", rol_delete.as_view(), name="rol_delete"),

    # CURSOS
    path("cursos/servicio/<int:servicio_id>/", curso_publico_lista.as_view(), name="cursos_por_servicio"),
    path("cursos/publico/<int:pk>/", CursoDetallePublicoView.as_view(), name="curso_detalle_publico"),
    path("cursos/", curso_lista.as_view(), name="curso_lista"),
    path("cursos/nuevo/", curso_create.as_view(), name="curso_create"),
    path("cursos/<int:pk>/editar/", curso_update.as_view(), name="curso_update"),
    path("cursos/<int:pk>/eliminar/", curso_delete.as_view(), name="curso_delete"),
    path("cursos/<int:pk>/", CursoDetalleView.as_view(), name="curso_detalle"),

    # USUARIOS
    path("usuarios/", usuario_lista.as_view(), name="usuario_lista"),
    path("usuarios/nuevo/", usuario_create, name="usuario_create"),
    path("usuarios/<int:pk>/editar/", usuario_update.as_view(), name="usuario_update"),
    path("usuarios/<int:pk>/eliminar/", usuario_delete.as_view(), name="usuario_delete"),

    # MATRÍCULAS
    path("matriculas/", MatriculaLista.as_view(), name="matricula_lista"),
    path("matriculas/nueva/", MatriculaCreate.as_view(), name="matricula_create"),
    path("matriculas/<int:pk>/editar/", MatriculaUpdate.as_view(), name="matricula_update"),
    path("matriculas/<int:pk>/eliminar/", MatriculaDelete.as_view(), name="matricula_delete"),

    # NOTAS
    path("notas/", nota_list, name="nota_list"),
    path("notas/nueva/", nota_create, name="nota_create"),
    path("notas/<int:pk>/editar/", nota_update, name="nota_update"),
    path("notas/<int:pk>/eliminar/", nota_delete, name="nota_delete"),
    path("notas/exportar/", nota_export, name="nota_export"),

    # ESPECIALIDAD
    path("especialidades/", especialidad_lista.as_view(), name="especialidad_lista"),
    path("especialidades/nueva/", especialidad_create.as_view(), name="especialidad_create"),
    path("especialidades/<int:pk>/editar/", especialidad_update.as_view(), name="especialidad_update"),
    path("especialidades/<int:pk>/eliminar/", especialidad_delete.as_view(), name="especialidad_delete"),

    # DOCENTE
    path("docentes/", docente_lista.as_view(), name="docente_lista"),
    path("docentes/nuevo/", docente_create.as_view(), name="docente_create"),
    path("docentes/<int:pk>/editar/", docente_update.as_view(), name="docente_update"),
    path("docentes/<int:pk>/eliminar/", docente_delete.as_view(), name="docente_delete"),


]
