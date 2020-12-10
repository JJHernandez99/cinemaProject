from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import Pelicula, Sala, Butaca, Proyeccion
from .serializers import PeliculaSerializer, SalaSerializer, ButacaSerializer, ProyeccionSerializer
from rest_framework.decorators import api_view
import datetime as dt


# Peliculas
@api_view(['GET', 'POST'])
def peliculas_list(request):
    if request.method == 'GET':
        # Devuelve peliculas con fecha valida en rango 10 dias antes y despues de la fecha actual
        fecha_actual = dt.datetime.now()
        ventana_tiempo = dt.timedelta(days=10)
        peliculas = Pelicula.objects.filter(fechaFin__gte=(fecha_actual - ventana_tiempo),
                                            fechaComienzo__lte=(fecha_actual + ventana_tiempo))
        peliculas_serializer = PeliculaSerializer(peliculas, many=True)
        return JsonResponse(peliculas_serializer.data, safe=False, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        pelicula_data = JSONParser().parse(request)
        pelicula_serializer = PeliculaSerializer(data=pelicula_data)
        if pelicula_serializer.is_valid():
            pelicula_serializer.save()
            return JsonResponse(pelicula_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(pelicula_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ***PENDIENTE*** Get pelicula + fecha
@api_view(['GET'])
def pelicula_detail(request, pk, ):
    try:
        pelicula = Pelicula.objects.get(pk=pk)

        if request.method == 'GET':
            pelicula_serializer = PeliculaSerializer(pelicula)
            return JsonResponse(pelicula_serializer.data, safe=False, status=status.HTTP_200_OK)

    except Pelicula.DoesNotExist:
        return JsonResponse({'Mensaje': 'La pelicula especificada no existe'}, status=status.HTTP_404_NOT_FOUND)


# Salas
@api_view(['GET', 'POST'])
def salas_list(request):
    if request.method == 'GET':
        salas = Sala.objects.all()
        salas_serializer = SalaSerializer(salas, many=True)
        return JsonResponse(salas_serializer.data, safe=False, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        salas_data = JSONParser().parse(request)
        salas_serializer = SalaSerializer(data=salas_data)
        if salas_serializer.is_valid():
            salas_serializer.save()
            return JsonResponse(salas_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(salas_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def sala_detail(request, pk):
    try:
        sala = Sala.objects.get(pk=pk)

        if request.method == 'GET':
            sala_serializer = SalaSerializer(sala)
            return JsonResponse(sala_serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'PUT':
            sala_data = JSONParser().parse(request)
            sala_serializer = SalaSerializer(sala, data=sala_data)
            if sala_serializer.is_valid():
                proyeccion = Proyeccion.objects.filter(sala=sala)
                if not (proyeccion.__sizeof__() != 0):
                    sala_serializer.save()
                    return JsonResponse(sala_serializer.data)
                return JsonResponse({'Mensaje': 'Sala asociada, elimine la proyeccion para editar la sala'})
            return JsonResponse(sala_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            sala.delete()
            return JsonResponse({'Mensaje': 'La sala se elimino correctamente'}, status=status.HTTP_204_NO_CONTENT)

    except Sala.DoesNotExist:
        return JsonResponse({'Mensaje': 'La sala especificada no existe'}, status=status.HTTP_404_NOT_FOUND)


# Proyecciones
@api_view(['GET', 'POST'])
def proyecciones_list(request, ):
    if request.method == 'GET':
        # cartelera
        fecha_actual = dt.date.today()
        proyecciones = Proyeccion.objects.filter(fechaInicio__lte=fecha_actual, fechaFin__gte=fecha_actual,
                                                 estado__exact=True)
        proyecciones_serializer = ProyeccionSerializer(proyecciones, many=True)
        return JsonResponse(proyecciones_serializer.data, safe=False, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        proyeccion_data = JSONParser().parse(request)
        proyeccion_serializer = ProyeccionSerializer(data=proyeccion_data)
        if proyeccion_serializer.is_valid():
            return corroborar_proyeccion(proyeccion_data, proyeccion_serializer)
        return JsonResponse(proyeccion_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def proyecciones_list_range(request, fecha):
    fecha_obj = dt.datetime.strptime(fecha, '%d-%m-%Y').date()
    if request.method == 'GET':
        proyecciones = Proyeccion.objects.filter(fechaInicio__lte=fecha_obj, fechaFin__gte=fecha_obj,
                                                 estado__exact=True)
        proyecciones_serializer = ProyeccionSerializer(proyecciones, many=True)
        return JsonResponse(proyecciones_serializer.data, safe=False, status=status.HTTP_200_OK)


# REALIZAR ESTE
@api_view(['GET'])
def proyeccion_detail_range(request, pk, fecha):
    fecha_obj = dt.datetime.strptime(fecha, '%d-%m-%Y').date()
    try:
        proyeccion = Proyeccion.objects.get(pk=pk)

        if request.method == 'GET':
            data = {}

            # proyeccion_serializer = ProyeccionSerializer(proyeccion, data=proyeccion_data)

    except Proyeccion.DoesNotExist:
        return JsonResponse({'Mensaje': 'La Proyeccion no existe'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def proyeccion_detail(request, pk, ):
    try:
        proyeccion = Proyeccion.objects.get(pk=pk)

        if request.method == 'PUT':
            proyeccion_data = JSONParser().parse(request)
            proyeccion_serializer = ProyeccionSerializer(proyeccion, data=proyeccion_data)
            if proyeccion_serializer.is_valid():
                return corroborar_proyeccion(proyeccion_data, proyeccion_serializer)
            return JsonResponse(proyeccion_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Proyeccion.DoesNotExist:
        return JsonResponse({'Mensaje': 'La Proyeccion no existe'}, status=status.HTTP_404_NOT_FOUND)


def corroborar_proyeccion(proyeccion_data, proyeccion_serializer):
    # Solo creo proyeccion si la peli esta hab , las fechas son validas, y la sala no esta deshab ni ocupada

    pelicula = Pelicula.objects.get(pk=proyeccion_data['pelicula'])
    sala = Sala.objects.get(pk=proyeccion_data['sala'])
    proyecciones = Proyeccion.objects.filter(sala=sala)
    fecha_inicio = dt.datetime.strptime(proyeccion_data['fechaInicio'], '%Y-%m-%d').date()
    fecha_fin = dt.datetime.strptime(proyeccion_data['fechaFin'], '%Y-%m-%d').date()
    if pelicula.estado:
        if sala.estado:
            if (pelicula.fechaComienzo <= fecha_inicio and
                    pelicula.fechaFin >= fecha_fin):
                for proyeccion in proyecciones:
                    if proyeccion.fechaInicio < fecha_inicio and proyeccion.fechaFin < fecha_inicio:
                        pass
                    elif proyeccion.fechaInicio > fecha_fin and proyeccion.fechaFin > fecha_fin:
                        pass
                    else:
                        return JsonResponse({'Mensaje': 'Sala ya ocupada en esas fechas'},
                                            status=status.HTTP_400_BAD_REQUEST)
                proyeccion_serializer.save()
                return JsonResponse(proyeccion_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse({'Mensaje': 'La sala esta deshabilitada'},
                            status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'Mensaje': 'La pelicula esta deshabilitada'},
                        status=status.HTTP_400_BAD_REQUEST)


# Butacas
@api_view(['GET', 'POST'])
def butacas_list(request):
    if request.method == 'GET':
        butacas = Butaca.objects.all()
        butacas_serializer = ButacaSerializer(butacas, many=True)
        return JsonResponse(butacas_serializer.data, safe=False, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        butaca_data = JSONParser().parse(request)
        butaca_serializer = ButacaSerializer(data=butaca_data)
        if butaca_serializer.is_valid():
            return corroborar_butaca(butaca_data, butaca_serializer)
        return JsonResponse(butaca_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
def butaca_detail(request, pk):
    try:
        butaca = Butaca.objects.get(pk=pk)

        if request.method == 'GET':
            butaca_serializer = ButacaSerializer(butaca)
            return JsonResponse(butaca_serializer.data, safe=False, status=status.HTTP_200_OK)

        elif request.method == 'PUT':
            butaca_data = JSONParser().parse(request)
            butaca_serializer = ButacaSerializer(butaca, data=butaca_data)
            if butaca_serializer.is_valid():
                return corroborar_butaca(butaca_data, butaca_serializer)
            return JsonResponse(butaca_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Butaca.DoesNotExist:
        return JsonResponse({'Mensaje': 'La Butaca especificada no existe'}, status=status.HTTP_404_NOT_FOUND)


def corroborar_butaca(butaca_data, butaca_serializer):
    proyeccion = Proyeccion.objects.get(pk=butaca_data['proyeccion'])
    if proyeccion.estado:
        sala = proyeccion.sala
        if butaca_data['fila'] <= sala.fila and butaca_data['asiento'] <= sala.asiento:
            butacas = Butaca.objects.filter(proyeccion=butaca_data['proyeccion'],
                                            fecha=dt.datetime.strptime(butaca_data['fecha'], '%Y-%m-%d').date())
            for butaca in butacas:
                if butaca.fila == butaca_data['fila'] and butaca.asiento == butaca_data['asiento']:
                    return JsonResponse({'Mensaje': 'La butaca deseada ya esta reservada'},
                                        status=status.HTTP_400_BAD_REQUEST)
            butaca_serializer.save()
            return JsonResponse(butaca_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse({'Mensaje': 'El numero de butaca es invalido para la sala seleccionada'},
                            status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'Mensaje': 'La proyeccion especificada esta inhabilitada para reservas'},
                        status=status.HTTP_400_BAD_REQUEST)
