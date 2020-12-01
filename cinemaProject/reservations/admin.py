from django.contrib import admin
from .models import Pelicula, Sala, Proyeccion, Butaca

# Register your models here.

admin.site.register(Pelicula)
admin.site.register(Sala)
admin.site.register(Proyeccion)
admin.site.register(Butaca)
