from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from .forms import ServicioForm, RolForm, CursoForm, UsuarioForm, BlogForm, MatriculaForm
from .models import Servicio, Rol, Curso, Usuario, Blog, Matricula
from django.contrib.auth import authenticate, login, logout


def login_view(request):
    if request.method == "POST":
        usuario = request.POST.get("usuario")   # 👈 coincide con USERNAME_FIELD
        password = request.POST.get("password")

        user = authenticate(request, usuario=usuario, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenido {user.nombres} {user.apellidos}")
            return redirect("inicio")  # 👈 redirige a tu página principal
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    return render(request, "registration/login.html")


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "Has cerrado sesión correctamente.")
        return super().dispatch(request, *args, **kwargs)


def inicio(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "core/inicio.html")


# ---------------- SERVICIO ----------------
class ServicioListView(LoginRequiredMixin, ListView):
    model = Servicio
    template_name = "core/servicio/lista.html"
    context_object_name = "servicios"
    paginate_by = 10
    ordering = ["nombre"]


class ServicioCreateView(LoginRequiredMixin, CreateView):
    model = Servicio
    form_class = ServicioForm
    template_name = "core/servicio/formulario.html"
    success_url = reverse_lazy("servicio_lista")

    def form_valid(self, form):
        messages.success(self.request, "Servicio registrado correctamente.")
        return super().form_valid(form)


class ServicioUpdateView(LoginRequiredMixin, UpdateView):
    model = Servicio
    form_class = ServicioForm
    template_name = "core/servicio/formulario.html"
    success_url = reverse_lazy("servicio_lista")

    def form_valid(self, form):
        messages.success(self.request, "Servicio actualizado correctamente.")
        return super().form_valid(form)


class ServicioDeleteView(LoginRequiredMixin, DeleteView):
    model = Servicio
    template_name = "core/servicio/eliminar.html"
    success_url = reverse_lazy("servicio_lista")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Servicio eliminado correctamente.")
        return super().delete(request, *args, **kwargs)


# ---------------- ROL ----------------
class rol_lista(LoginRequiredMixin, ListView):
    model = Rol
    template_name = "core/rol/rol_lista.html"
    context_object_name = "roles"
    paginate_by = 10
    ordering = ["nombre"]


class rol_create(LoginRequiredMixin, CreateView):
    model = Rol
    form_class = RolForm
    template_name = "core/rol/rol_form.html"
    success_url = reverse_lazy("rol_lista")

    def form_valid(self, form):
        messages.success(self.request, "Rol registrado correctamente.")
        return super().form_valid(form)


class rol_update(LoginRequiredMixin, UpdateView):
    model = Rol
    form_class = RolForm
    template_name = "core/rol/rol_form.html"
    success_url = reverse_lazy("rol_lista")

    def form_valid(self, form):
        messages.success(self.request, "Rol actualizado correctamente.")
        return super().form_valid(form)


class rol_delete(LoginRequiredMixin, DeleteView):
    model = Rol
    template_name = "core/rol/rol_eliminar.html"
    success_url = reverse_lazy("rol_lista")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Rol eliminado correctamente.")
        return super().delete(request, *args, **kwargs)


# ---------------- CURSO ----------------
class curso_lista(LoginRequiredMixin, ListView):
    model = Curso
    template_name = "core/curso/curso_lista.html"
    context_object_name = "cursos"
    paginate_by = 10
    ordering = ["nombre_curso"]


class curso_create(LoginRequiredMixin, CreateView):
    model = Curso
    form_class = CursoForm
    template_name = "core/curso/curso_form.html"
    success_url = reverse_lazy("curso_lista")

    def form_valid(self, form):
        messages.success(self.request, "Curso registrado correctamente.")
        return super().form_valid(form)


class curso_update(LoginRequiredMixin, UpdateView):
    model = Curso
    form_class = CursoForm
    template_name = "core/curso/curso_form.html"
    success_url = reverse_lazy("curso_lista")

    def form_valid(self, form):
        messages.success(self.request, "Curso actualizado correctamente.")
        return super().form_valid(form)


class curso_delete(LoginRequiredMixin, DeleteView):
    model = Curso
    template_name = "core/curso/curso_eliminar.html"
    success_url = reverse_lazy("curso_lista")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Curso eliminado correctamente.")
        return super().delete(request, *args, **kwargs)


# ---------------- USUARIO ----------------
class usuario_lista(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = "core/usuario/usuario_lista.html"
    context_object_name = "usuarios"
    paginate_by = 10
    ordering = ["apellidos", "nombres"]


def usuario_create(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            nueva_password = form.cleaned_data.get("password")

            # ✅ Encriptamos solo si se ingresó una contraseña
            if nueva_password:
                usuario.set_password(nueva_password)

            usuario.save()
            messages.success(request, "Usuario creado correctamente.")
            return redirect("usuario_lista")
        else:
            messages.error(request, "Hubo un error al crear el usuario.")
    else:
        form = UsuarioForm()

    return render(request, "core/usuario/usuario_form.html", {"form": form})


class usuario_update(LoginRequiredMixin, UpdateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = "core/usuario/usuario_form.html"
    success_url = reverse_lazy("usuario_lista")

    def form_valid(self, form):
        usuario = form.save(commit=False)
        nueva_password = form.cleaned_data.get("password")

        # ✅ Solo encriptamos si el usuario ingresó una nueva contraseña
        if nueva_password:
            usuario.set_password(nueva_password)

        usuario.save()
        messages.success(self.request, "Usuario actualizado correctamente.")
        return redirect("usuario_lista")


class usuario_delete(LoginRequiredMixin, DeleteView):
    model = Usuario
    template_name = "core/usuario/usuario_eliminar.html"
    success_url = reverse_lazy("usuario_lista")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Usuario eliminado correctamente.")
        return super().delete(request, *args, **kwargs)


# ---------------- BLOG ----------------
class blog_lista(ListView):
    model = Blog
    template_name = "core/blog/blog_lista.html"
    context_object_name = "blogs"
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        servicio_id = self.kwargs.get("servicio_id")
        if servicio_id:
            queryset = queryset.filter(servicio_id=servicio_id)
        return queryset


class blog_create(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    template_name = "core/blog/blog_form.html"
    success_url = reverse_lazy("blog_lista")

    def form_valid(self, form):
        messages.success(self.request, "Blog creado correctamente.")
        return super().form_valid(form)


class blog_update(LoginRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = "core/blog/blog_form.html"
    success_url = reverse_lazy("blog_lista")

    def form_valid(self, form):
        messages.success(self.request, "Blog actualizado correctamente.")
        return super().form_valid(form)


class blog_delete(LoginRequiredMixin, DeleteView):
    model = Blog
    template_name = "core/blog/blog_eliminar.html"
    success_url = reverse_lazy("blog_lista")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Blog eliminado correctamente.")
        return super().delete(request, *args, **kwargs)


class blog_detalle(DetailView):
    model = Blog
    template_name = "core/blog/blog_detalle.html"
    context_object_name = "blog"


# ---------------- SERVICIO PÚBLICO ----------------
class servicio_publico_lista(ListView):
    model = Servicio
    template_name = "core/servicio/servicio_publico.html"
    context_object_name = "servicios"


# ---------------- MATRÍCULA ----------------
class MatriculaLista(ListView):
    model = Matricula
    template_name = "core/matricula/matricula_lista.html"
    context_object_name = "matriculas"


class MatriculaCreate(CreateView):
    model = Matricula
    form_class = MatriculaForm
    template_name = "core/matricula/matricula_form.html"
    success_url = reverse_lazy("matricula_lista")


class MatriculaUpdate(UpdateView):
    model = Matricula
    form_class = MatriculaForm
    template_name = "core/matricula/matricula_form.html"
    success_url = reverse_lazy("matricula_lista")


class MatriculaDelete(DeleteView):
    model = Matricula
    template_name = "core/matricula/matricula_delete.html"
    success_url = reverse_lazy("matricula_lista")
