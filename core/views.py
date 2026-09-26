from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from .forms import ServicioForm, RolForm, CursoForm, UsuarioForm, BlogForm, MatriculaForm, NotaForm, EspecialidadForm,DocenteForm
from .models import Servicio, Rol, Curso, Usuario, Blog, Matricula, Nota, Especialidad,Docente
from django.contrib.auth import authenticate, login, logout
import openpyxl
from django.http import HttpResponse


def login_view(request):
    if request.method == "POST":
        usuario = request.POST.get("usuario")
        password = request.POST.get("password")

        user = authenticate(request, usuario=usuario, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenido {user.nombres} {user.apellidos}")
            return redirect("inicio")
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

    def get_queryset(self):
        # ✅ Incluimos docente y especialidad en la consulta para optimizar
        return Curso.objects.select_related("servicio", "docente__idEspecialidad").all()


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


# ✅ CURSO PÚBLICO (filtrado por servicio)
class curso_publico_lista(ListView):
    model = Curso
    template_name = "core/curso/curso_lista_publica.html"
    context_object_name = "cursos"
    paginate_by = 10
    ordering = ["nombre_curso"]

    def get_queryset(self):
        servicio_id = self.kwargs.get("servicio_id")
        return Curso.objects.filter(servicio_id=servicio_id).select_related("docente__idEspecialidad")


# ✅ DETALLE DE CURSO (privado)
class CursoDetalleView(DetailView):
    model = Curso
    template_name = "core/curso/curso_detalle.html"
    context_object_name = "curso"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ✅ Añadimos docente y especialidad al contexto
        context["docente"] = self.object.docente
        context["especialidad"] = self.object.docente.idEspecialidad if self.object.docente else None
        return context


# ✅ DETALLE DE CURSO PÚBLICO
class CursoDetallePublicoView(DetailView):
    model = Curso
    template_name = "core/curso/curso_detalle_publico.html"
    context_object_name = "curso"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["servicio"] = self.object.servicio
        context["docente"] = self.object.docente
        context["especialidad"] = self.object.docente.idEspecialidad if self.object.docente else None
        return context



# ---------------- USUARIO ----------------
class usuario_lista(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = "core/usuario/usuario_lista.html"
    context_object_name = "usuarios"
    paginate_by = 10
    ordering = ["apellidos", "nombres"]

# ... (resto de usuarios, blogs, servicio_publico_lista y matrículas igual que antes)



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


# ✅ DETALLE DE BLOG (privado)
class blog_detalle(DetailView):
    model = Blog
    template_name = "core/blog/blog_detalle.html"
    context_object_name = "blog"


# ✅ NUEVO: BLOG PÚBLICO (filtrado por servicio)
class blog_publico_lista(ListView):
    model = Blog
    template_name = "core/blog/blog_lista_publica.html"
    context_object_name = "blogs"
    paginate_by = 6

    def get_queryset(self):
        servicio_id = self.kwargs.get("servicio_id")
        return Blog.objects.filter(servicio_id=servicio_id)


# ✅ DETALLE DE BLOG PÚBLICO
class BlogDetallePublicoView(DetailView):
    model = Blog
    template_name = "core/blog/blog_detalle_publico.html"  # plantilla separada para público
    context_object_name = "blog"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pasamos también el servicio para que el botón "Volver a lista" sepa a dónde regresar
        context["servicio"] = self.object.servicio
        return context


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

# ---------------- NOTA ----------------
def nota_list(request):
    notas = Nota.objects.all()

    alumno_id = request.GET.get('alumno')
    curso_id = request.GET.get('curso')

    if alumno_id:
        notas = notas.filter(idmatricula__usuario__id=alumno_id)
    if curso_id:
        notas = notas.filter(idmatricula__curso__id=curso_id)

    # Paginación: 10 notas por página
    paginator = Paginator(notas, 10)
    page_number = request.GET.get('page')
    notas_page = paginator.get_page(page_number)

    alumnos = Usuario.objects.all()
    cursos = Curso.objects.all()

    return render(request, 'core/nota/nota_lista.html', {
        'notas': notas_page,
        'alumnos': alumnos,
        'cursos': cursos,
    })


def nota_create(request):
    if request.method == 'POST':
        form = NotaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nota_list')
    else:
        form = NotaForm()
    return render(request, 'core/nota/nota_form.html', {'form': form})


def nota_update(request, pk):
    nota = get_object_or_404(Nota, pk=pk)
    if request.method == 'POST':
        form = NotaForm(request.POST, instance=nota)
        if form.is_valid():
            form.save()
            return redirect('nota_list')
    else:
        form = NotaForm(instance=nota)
    return render(request, 'core/nota/nota_form.html', {'form': form})


def nota_delete(request, pk):
    nota = get_object_or_404(Nota, pk=pk)
    if request.method == 'POST':
        nota.delete()
        return redirect('nota_list')
    return render(request, 'nota_eliminar.html', {'nota': nota})


def nota_export(request):
    notas = Nota.objects.all()

    alumno_id = request.GET.get('alumno')
    curso_id = request.GET.get('curso')

    if alumno_id:
        notas = notas.filter(idmatricula__usuario__id=alumno_id)
    if curso_id:
        notas = notas.filter(idmatricula__curso__id=curso_id)

    # Crear archivo Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Notas"

    # Encabezados en negrita
    headers = ['ID', 'Alumno', 'Curso', 'Valor Nota', 'Fecha Creación']
    ws.append(headers)
    for cell in ws[1]:
        cell.font = openpyxl.styles.Font(bold=True)

    # Datos
    for nota in notas:
        ws.append([
            nota.idnota,
            nota.idmatricula.usuario.nombres,
            nota.idmatricula.curso.nombre_curso,
            nota.valor_nota,
            nota.fec_crea.strftime("%Y-%m-%d")
        ])

    # Ajustar ancho de columnas
    for column_cells in ws.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        ws.column_dimensions[column_cells[0].column_letter].width = length + 2

    # Respuesta HTTP
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="notas.xlsx"'
    wb.save(response)
    return response

# ---------------- ESCPECIALIDAD ----------------
class especialidad_lista(LoginRequiredMixin, ListView):
    model = Especialidad
    template_name = "core/especialidad/especialidad_lista.html"
    context_object_name = "especialidades"
    paginate_by = 10
    ordering = ["nomEspecialidad"]

class especialidad_create(LoginRequiredMixin, CreateView):
    model = Especialidad
    form_class = EspecialidadForm
    template_name = "core/especialidad/especialidad_form.html"
    success_url = reverse_lazy("especialidad_lista")

    def form_valid(self, form):
        messages.success(self.request, "Especialidad registrada correctamente.")
        return super().form_valid(form)

class especialidad_update(LoginRequiredMixin, UpdateView):
    model = Especialidad
    form_class = EspecialidadForm
    template_name = "core/especialidad/especialidad_form.html"
    success_url = reverse_lazy("especialidad_lista")

    def form_valid(self, form):
        messages.success(self.request, "Especialidad actualizada correctamente.")
        return super().form_valid(form)

class especialidad_delete(LoginRequiredMixin, DeleteView):
    model = Especialidad
    template_name = "core/especialidad/especialidad_eliminar.html"
    success_url = reverse_lazy("especialidad_lista")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Especialidad eliminada correctamente.")
        return super().delete(request, *args, **kwargs)

# ---------------- DOCENTE ----------------
class docente_lista(LoginRequiredMixin, ListView):
    model = Docente
    template_name = "core/docente/docente_lista.html"
    context_object_name = "docentes"
    paginate_by = 10
    ordering = ["apePaterno", "priNombre"]

class docente_create(LoginRequiredMixin, CreateView):
    model = Docente
    form_class = DocenteForm
    template_name = "core/docente/docente_form.html"
    success_url = reverse_lazy("docente_lista")

    def form_valid(self, form):
        messages.success(self.request, "Docente registrado correctamente.")
        return super().form_valid(form)

class docente_update(LoginRequiredMixin, UpdateView):
    model = Docente
    form_class = DocenteForm
    template_name = "core/docente/docente_form.html"
    success_url = reverse_lazy("docente_lista")

    def form_valid(self, form):
        messages.success(self.request, "Docente actualizado correctamente.")
        return super().form_valid(form)

class docente_delete(LoginRequiredMixin, DeleteView):
    model = Docente
    template_name = "core/docente/docente_eliminar.html"
    success_url = reverse_lazy("docente_lista")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Docente eliminado correctamente.")
        return super().delete(request, *args, **kwargs)