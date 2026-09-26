# Importa el panel de administración de Django
from django.contrib import admin

# Importa las funciones para definir rutas (path, include)
from django.urls import path, include

# Importa las vistas de autenticación que ya trae Django (login/logout)
from django.contrib.auth import views as auth_views

# Importa tu vista personalizada de logout desde la app core
from core.views import CustomLogoutView


urlpatterns = [
    # 👉 Ruta para el panel de administración de Django
    path("admin/", admin.site.urls),

    # 👉 Ruta para el login (usa la vista de Django pero con tu template personalizado)
    path("accounts/login/", 
         auth_views.LoginView.as_view(template_name="registration/login.html"), 
         name="login"),

    # 👉 Ruta para el logout (usa tu vista CustomLogoutView)
    path("accounts/logout/", 
         CustomLogoutView.as_view(next_page="login"), 
         name="logout"),

    # 👉 Incluye todas las rutas definidas en core/urls.py
    # Esto significa que la raíz "/" (127.0.0.1:8000/) se resuelve con las rutas de la app core
    path("", include("core.urls")),
]


# 👉 Configuración para servir archivos multimedia (imágenes, documentos, etc.)
# Solo se activa cuando estás en modo DEBUG (desarrollo)
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
