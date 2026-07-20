from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class Rol(models.Model):
    nombre = models.CharField(max_length=100, unique=True, null=True, blank=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre if self.nombre else "Sin nombre"


class UsuarioManager(BaseUserManager):
    def create_user(self, usuario, password=None, **extra_fields):
        if not usuario:
            raise ValueError("El campo usuario es obligatorio")
        user = self.model(usuario=usuario, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, usuario, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # ✅ Si no se pasa rol, asignamos el rol con id=1
        if "rol" not in extra_fields or extra_fields["rol"] is None:
            try:
                rol_default = Rol.objects.get(pk=1)
            except Rol.DoesNotExist:
                # Creamos el rol por defecto si no existe
                rol_default = Rol.objects.create(
                    id=1,
                    nombre="Administrador",
                    descripcion="Rol por defecto para superusuarios"
                )
            extra_fields["rol"] = rol_default

        return self.create_user(usuario, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    ESTADOS_USUARIO = [
        ("activo", "Activo"),
        ("inactivo", "Inactivo"),
    ]

    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, related_name="usuarios")
    usuario = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=128, null=True, blank=True)  # ✅ campo correcto
    estado = models.CharField(max_length=200, choices=ESTADOS_USUARIO, default="activo")
    apellidos = models.CharField(max_length=200)
    nombres = models.CharField(max_length=200)
    correo = models.EmailField(max_length=200, unique=True)
    telefono = models.CharField(max_length=200, validators=[RegexValidator(r'^\+?\d{7,15}$')])
    direccion = models.CharField(max_length=200)

    # Campos requeridos por Django
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "usuario"
    REQUIRED_FIELDS = ["correo", "nombres", "apellidos"]

    objects = UsuarioManager()

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class Servicio(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=500)
    imagenservicio = models.ImageField(
        upload_to="servicios/",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.nombre


class Curso(models.Model):
    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.PROTECT,
        related_name="cursos"
    )
    nombre_curso = models.CharField(max_length=200)
    costo = models.DecimalField(
        max_digits=9,
        decimal_places=4,
        validators=[MinValueValidator(0)]
    )
    descripcion = models.CharField(max_length=500)

    def __str__(self):
        return self.nombre_curso


class Blog(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="blogs"
    )
    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.PROTECT,
        related_name="blogs"
    )
    titulo = models.CharField(max_length=500)
    textoblog = models.TextField()
    imagenblog = models.ImageField(
        upload_to="blogs/",
        blank=True,
        null=True
    )
    fecha_publicacion = models.DateField()

    def __str__(self):
        return self.titulo


class Matricula(models.Model):
    ESTADOS_MATRICULA = [
        ("pendiente", "Pendiente"),
        ("activa", "Activa"),
        ("finalizada", "Finalizada"),
    ]

    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name="matriculas"
    )
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="matriculas"
    )
    fecha_matricula = models.DateField()
    estado_matricula = models.CharField(max_length=30, choices=ESTADOS_MATRICULA, default="pendiente")
    nota_final = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.usuario} - {self.curso}"
