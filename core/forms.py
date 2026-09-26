from django import forms
from .models import Servicio, Rol, Curso, Usuario, Blog, Matricula, Docente, Nota, Especialidad

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ["nombre", "descripcion", "imagenservicio"]

        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "imagenservicio": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

        help_texts = {
            "nombre": "Ingrese el nombre del servicio.",
            "descripcion": "Describa brevemente el servicio.",
            "imagenservicio": "Opcional: suba una imagen representativa.",
        }


class RolForm(forms.ModelForm):
    class Meta:
        model = Rol
        fields = ["nombre", "descripcion"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class CursoForm(forms.ModelForm):
    docente = forms.ModelChoiceField(
        queryset=Docente.objects.all(),
        required=True,
        widget=forms.Select(attrs={"class": "form-select"})
    )

    class Meta:
        model = Curso
        fields = ["servicio", "docente", "nombre_curso", "costo", "descripcion"]
        widgets = {
            "servicio": forms.Select(attrs={"class": "form-select"}),
            "nombre_curso": forms.TextInput(attrs={"class": "form-control"}),
            "costo": forms.NumberInput(attrs={"class": "form-control", "step": "0.0001"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control w-100", "rows": 6}),
        }


class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=False,  # ✅ al editar no es obligatorio
    )

    class Meta:
        model = Usuario
        fields = [
            "rol",
            "usuario",
            "password",
            "estado",
            "apellidos",
            "nombres",
            "correo",
            "telefono",
            "direccion",
        ]
        widgets = {
            "rol": forms.Select(attrs={"class": "form-select"}),
            "usuario": forms.TextInput(attrs={"class": "form-control"}),
            "estado": forms.Select(attrs={"class": "form-select"}),
            "apellidos": forms.TextInput(attrs={"class": "form-control"}),
            "nombres": forms.TextInput(attrs={"class": "form-control"}),
            "correo": forms.EmailInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "direccion": forms.TextInput(attrs={"class": "form-control"}),
        }


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = [
            "usuario",
            "servicio",
            "titulo",
            "textoblog",
            "imagenblog",
            "fecha_publicacion",
        ]
        widgets = {
            "usuario": forms.Select(attrs={"class": "form-select"}),
            "servicio": forms.Select(attrs={"class": "form-select"}),
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "textoblog": forms.Textarea(attrs={"class": "form-control w-100", "rows": 6}),
            "imagenblog": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "fecha_publicacion": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }


class MatriculaForm(forms.ModelForm):
    class Meta:
        model = Matricula
        fields = ["curso", "usuario", "fecha_matricula", "estado_matricula", "nota_final"]
        widgets = {
            "curso": forms.Select(attrs={"class": "form-select"}),
            "usuario": forms.Select(attrs={"class": "form-select"}),
            "fecha_matricula": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "estado_matricula": forms.Select(attrs={"class": "form-select"}),
            "nota_final": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        }


class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['idmatricula', 'valor_nota', 'fec_crea']
        widgets = {
            'idmatricula': forms.Select(attrs={'class': 'form-select'}),
            'valor_nota': forms.NumberInput(attrs={'class': 'form-control'}),
            'fec_crea': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = ['nomEspecialidad']
        widgets = {
            'nomEspecialidad': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DocenteForm(forms.ModelForm):
    class Meta:
        model = Docente
        fields = [
            'idEspecialidad', 'priNombre', 'segNombre', 'terNombre',
            'apePaterno', 'apeMaterno', 'dni', 'direccion', 'telefono'
        ]
        widgets = {
            'idEspecialidad': forms.Select(attrs={'class': 'form-select'}),
            'priNombre': forms.TextInput(attrs={'class': 'form-control'}),
            'segNombre': forms.TextInput(attrs={'class': 'form-control'}),
            'terNombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apePaterno': forms.TextInput(attrs={'class': 'form-control'}),
            'apeMaterno': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }


