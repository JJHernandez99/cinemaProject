from rest_framework import serializers
from reservations.models import Pelicula, Proyeccion, Butaca, Sala


class PeliculaSerializer(serializers.ModelSerializer):

    class Meta:
        model = 'Pelicula'
        fields = ('id', 'duracion', 'descripcion', 'detalle', 'genero', 'clasificacion', 'estado', 'fechaComienzo', 'fechaFin')


class ProyeccionSerializer(serializers.ModelSerializer):

    class Meta:
        model = 'Proyeccion'
        fields = ('sala', 'pelicula', 'fechaInicio', 'fechaFin', 'horaProyeccion', 'estado')


class SalaSerializer(serializers.ModelSerializer):

    class Meta:
        model = 'Sala'
        fields = ('nombre', 'estado', 'fila', 'asiento')


class ButacaSerializer(serializers.ModelSerializer):

    class Meta:
        model = 'Butaca'
        fields = ('proyeccion', 'fecha', 'fila', 'asiento')
