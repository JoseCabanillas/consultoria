from django.urls import path
from .views import (
    usuario_lista, usuario_create, usuario_update, usuario_delete,
    curso_lista, curso_create, curso_update, curso_delete,
    rol_lista, rol_create, rol_update, rol_delete,
    ServicioListView, ServicioCreateView, ServicioUpdateView, ServicioDeleteView,
    servicio_publico_lista,
    blog_lista, blog_create, blog_update, blog_delete, blog_detalle,
    MatriculaLista, MatriculaCreate, MatriculaDelete, MatriculaUpdate,
    inicio, login_view, CustomLogoutView,
)

urlpatterns = [
    # Página pública (raíz del sitio)
    path("", servicio_publico_lista.as_view(), name="servicio_publico"),

    # Página privada de inicio (después de login)
    path("inicio/", inicio, name="inicio"),

    # Blog por servicio
    path("blogs/servicio/<int:servicio_id>/", blog_lista.as_view(), name="blogs_por_servicio"),

    # Login y logout (usando tus vistas personalizadas)
    path("login/", login_view, name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),

    # CRUD de Servicios
    path("servicios/", ServicioListView.as_view(), name="servicio_lista"),
    path("servicios/nuevo/", ServicioCreateView.as_view(), name="servicio_create"),
    path("servicios/<int:pk>/editar/", ServicioUpdateView.as_view(), name="servicio_update"),
    path("servicios/<int:pk>/eliminar/", ServicioDeleteView.as_view(), name="servicio_delete"),

    # CRUD de Rol
    path("roles/", rol_lista.as_view(), name="rol_lista"),
    path("roles/nuevo/", rol_create.as_view(), name="rol_create"),
    path("roles/<int:pk>/editar/", rol_update.as_view(), name="rol_update"),
    path("roles/<int:pk>/eliminar/", rol_delete.as_view(), name="rol_delete"),

    # CRUD de Curso
    path("cursos/", curso_lista.as_view(), name="curso_lista"),
    path("cursos/nuevo/", curso_create.as_view(), name="curso_create"),
    path("cursos/<int:pk>/editar/", curso_update.as_view(), name="curso_update"),
    path("cursos/<int:pk>/eliminar/", curso_delete.as_view(), name="curso_delete"),

    # CRUD de Usuario
    path("usuarios/", usuario_lista.as_view(), name="usuario_lista"),
    path("usuarios/nuevo/", usuario_create, name="usuario_create"),  # función
    path("usuarios/<int:pk>/editar/", usuario_update.as_view(), name="usuario_update"),
    path("usuarios/<int:pk>/eliminar/", usuario_delete.as_view(), name="usuario_delete"),

    # CRUD de Blog
    path("blogs/", blog_lista.as_view(), name="blog_lista"),
    path("blogs/nuevo/", blog_create.as_view(), name="blog_create"),
    path("blogs/<int:pk>/editar/", blog_update.as_view(), name="blog_update"),
    path("blogs/<int:pk>/eliminar/", blog_delete.as_view(), name="blog_delete"),
    path("blogs/<int:pk>/", blog_detalle.as_view(), name="blog_detalle"),

    # CRUD de Matricula
    path("matriculas/", MatriculaLista.as_view(), name="matricula_lista"),
    path("matriculas/nueva/", MatriculaCreate.as_view(), name="matricula_create"),
    path("matriculas/<int:pk>/editar/", MatriculaUpdate.as_view(), name="matricula_update"),
    path("matriculas/<int:pk>/eliminar/", MatriculaDelete.as_view(), name="matricula_delete"),
]
