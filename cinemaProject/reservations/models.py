from django.db import models

# Create your models here.

class Pelicula (models.Model):
    nombre=models.CharField(max_length=30,help_text="Nombre de la pelicula")
    duracion=models.IntegerField