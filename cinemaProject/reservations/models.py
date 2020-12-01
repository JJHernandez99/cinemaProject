from django.db import models

# Create your models here.


class Pelicula (models.Model):
    nombre = models.CharField(max_length=30, help_text="Nombre de la pelicula")
    duracion = models.IntegerField(help_text="Duracion de la pelicula en minutos")
    descripcion = models.TextField()
    detalle = models.TextField()
    genero = models.CharField(max_length=20)
    clasificacion = models.CharField(max_length=20)
    estado = models.BooleanField(default=False)
    fechaComienzo = models.DateField()
    fechaFin = models.DateField()


class Sala (models.Model):
    nombre = models.CharField(max_length=30, help_text="Nombre de la sala")
    estado = models.CharField(max_length=20)
    fila = models.IntegerField()
    asiento = models.IntegerField()


class Proyeccion (models.Model):
    sala = models.ForeignKey('Sala', on_delete=models.CASCADE, )
    pelicula = models.ForeignKey('Pelicula', on_delete=models.CASCADE, )
    fechaInicio = models.DateField()
    fechaFin = models.DateField()
    horaProyeccion = models.TimeField()
    estado = models.CharField(max_length=20)


class Butaca(models.Model):
    proyeccion = models.ForeignKey('Proyeccion', on_delete=models.CASCADE,)
    fecha = models.DateTimeField(auto_now_add=True)
    fila = models.IntegerField()
    asiento = models.IntegerField()
