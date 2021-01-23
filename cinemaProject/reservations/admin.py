from django.contrib import admin
from .models import Pelicula, Sala, Butaca, Proyeccion


class PeliculasAdmin(admin.ModelAdmin):
    list_display = ("id","nombre", "fechaComienzo", "fechaFinalizacion", "estado")

class SalasAdmin(admin.ModelAdmin):
    list_display = ("id","nombre", "estado","fila","asiento")


class ProyeccionesAdmin(admin.ModelAdmin):
    list_display = ("id","pelicula", "sala", "estado","fechaInicio","fechaFin")


class ButacasAdmin(admin.ModelAdmin):
    list_display = ("id","proyeccion", "fecha", "fila", "asiento")


admin.site.register(Pelicula, PeliculasAdmin)
admin.site.register(Sala, SalasAdmin)
admin.site.register(Butaca, ButacasAdmin)
admin.site.register(Proyeccion, ProyeccionesAdmin)
