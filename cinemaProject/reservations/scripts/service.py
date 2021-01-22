import datetime as dt
from reservations.models import Pelicula
import requests


def run():
    actualizar_db()


def actualizar_db():
    # Acceso al servicio web de peliculas
    r = requests.get('http://localhost:5000/api/pelicula/')
    peliculas_servicio = r.json()

    # Acceso a la bd de peliculas
    peliculas_db = list(Pelicula.objects.all().values())

    # Adaptamos los datos a nustra BD
    peliculas_servicio = adaptar_servicio(peliculas_servicio)
    peliculas_db = eliminar_id(peliculas_db)

    # Actualizacion propia de la bd
    for pelicula in peliculas_servicio:
        if pelicula not in peliculas_db:
            Pelicula.objects.update_or_create(nombre=pelicula['nombre'],
                                              defaults={
                                                  'duracion': pelicula['duracion'],
                                                  'descripcion': pelicula['descripcion'],
                                                  'detalle': pelicula['detalle'],
                                                  'genero': pelicula['genero'],
                                                  'clasificacion': pelicula['clasificacion'],
                                                  'estado': pelicula['estado'],
                                                  'fechaComienzo': pelicula['fechaComienzo'],
                                                  'fechaFinalizacion': pelicula['fechaFinalizacion']
                                              })

    # Ponemos inactivas las peliculas que no figuren en el servicio
    peliculas_db = list(Pelicula.objects.all().values())
    peliculas_db = eliminar_id(peliculas_db)
    for pelicula in peliculas_db:
        if pelicula not in peliculas_servicio:
            Pelicula.objects.filter(nombre=pelicula['nombre']).update(estado=False)


def adaptar_servicio(peliculas_servicio):
    for pelicula in peliculas_servicio:
        del pelicula['id']
        pelicula['fechaComienzo'] = dt.datetime.strptime(pelicula['fechaComienzo'], '%Y-%m-%dT%H:%M:%S+%f').date()
        pelicula['fechaFinalizacion'] = dt.datetime.strptime(pelicula['fechaFinalizacion'],
                                                             '%Y-%m-%dT%H:%M:%S+%f').date()
        if (pelicula['estado'] == "Activa"):
            pelicula['estado'] = True
        else:
            pelicula['estado'] = False

    return peliculas_servicio


def eliminar_id(peliculas_lista):
    for pelicula in peliculas_lista:
        del pelicula['id']

    return peliculas_lista
