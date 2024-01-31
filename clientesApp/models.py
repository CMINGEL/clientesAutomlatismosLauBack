from django.db import models
from django.contrib.auth.models import AbstractUser

def user_directory_path(instance, filename):
    return './{0}/{1}'.format(instance.cliente_id, filename)

class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]

class Servicio(models.Model):
    tipoServicio = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tipoServicio
        #return str(self.id)

class cliente(models.Model):
    
    nombre=models.CharField(max_length=50, null=True, blank= True)
    numeroContacto=models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    tipoContrato = models.CharField(max_length=50, null=True, blank=True)
    fechaInicioContrato=models.DateTimeField(null=True, blank=True)
    fechaFinContrato=models.DateTimeField(null=True, blank=True)
    fechaCreacion=models.DateTimeField(auto_now_add=True)
    ejecutivoCierre = models.CharField(max_length=50, null=True, blank=True)
    ejecutivoActual = models.CharField(max_length=50, null=True, blank=True)
    desistido = models.BooleanField(default=False)
    servicios = models.ManyToManyField(Servicio)

    class Meta:
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'

    def __str__(self):
        return self.nombre

class ejecutivo(models.Model):
    nombre=models.CharField(max_length=50)
    activo=models.BooleanField(default=True)
    fechaCreacion=models.DateTimeField(auto_now_add=True, null=True, blank=True)

class Archivo(models.Model):
    cliente = models.ForeignKey(cliente, null=True, blank=True, on_delete=models.CASCADE)
    image_content = models.FileField(upload_to=user_directory_path, blank=True, null=True)

    def __str__(self):
        return self.image_content
    
    class Meta:
        verbose_name = 'archivo'
