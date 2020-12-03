from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import Pelicula, Sala, Butaca, Proyeccion
from .serializers import PeliculaSerializer, SalaSerializer, ButacaSerializer, ProyeccionSerializer
from rest_framework.decorators import api_view
import datetime as dt


# Peliculas - Listo
@api_view(['GET', 'POST'])
def peliculas_list(request):
    if request.method == 'GET':
        fecha_actual = dt.datetime.now()
        ventana_tiempo = dt.timedelta(days=10)
        pelicula = Pelicula.objects.filter(fechaFin__gte=(fecha_actual - ventana_tiempo),
                                           fechaComienzo__lte=(fecha_actual + ventana_tiempo))
        # pelicula=Pelicula.objects.all() trae todas las peliculas
        peliculas_serializer = PeliculaSerializer(pelicula, many=True)
        return JsonResponse(peliculas_serializer.data, safe=False, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        pelicula_data = JSONParser().parse(request)
        pelicula_serializer = PeliculaSerializer(data=pelicula_data)
        if pelicula_serializer.is_valid():
            pelicula_serializer.save()
            return JsonResponse(pelicula_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(pelicula_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Get pelicula + fecha -- Debemos traer los dias de la proyeccion
@api_view(['GET'])
def pelicula_detail(request, pk, ):
    try:
        pelicula = Pelicula.objects.get(pk=pk)

        if request.method == 'GET':
            pelicula_serializer = PeliculaSerializer(pelicula)
            return JsonResponse(pelicula_serializer.data, safe=False, status=status.HTTP_200_OK)

        elif request.method == 'DELETE':
            pelicula.delete()
            return JsonResponse({'Mensaje': 'La pelicula se elimino correctamente'}, status=status.HTTP_204_NO_CONTENT)

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
        else:
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
                sala_serializer.save()
                return JsonResponse(sala_serializer.data)
            return JsonResponse(sala_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            sala.delete()
            return JsonResponse({'Mensaje': 'La sala se elimino correctamente'}, status=status.HTTP_204_NO_CONTENT)

    except Sala.DoesNotExist:
        return JsonResponse({'Mensaje': 'La sala especificada no existe'}, status=status.HTTP_404_NOT_FOUND)


# Proyecciones
@api_view(['GET', 'POST'])
def proyecciones_list(request, ):
    fecha_actual = dt.date.today()
    if request.method == 'GET':
        proyecciones = Proyeccion.objects.all()
        proyecciones_pos = []
        for proyeccion in proyecciones:
            pelicula = Pelicula.objects.get(id=proyeccion.pelicula.pk, )
            if pelicula.estado:
                if pelicula.fechaFin > fecha_actual >= pelicula.fechaComienzo:
                    proyecciones_pos.append(proyeccion)
        proyecciones_serializer = ProyeccionSerializer(proyecciones_pos, many=True)
        return JsonResponse(proyecciones_serializer.data, safe=False, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        proyeccion_data = JSONParser().parse(request)
        proyeccion_serializer = ProyeccionSerializer(data=proyeccion_data)
        if proyeccion_serializer.is_valid():
            proyeccion_serializer.save()
            return JsonResponse(proyeccion_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def proyecciones_list_range(request, fecha):
    fecha_obj = dt.datetime.strptime(fecha, '%d-%m-%Y').date()
    if request.method == 'GET':
        proyecciones = Proyeccion.objects.all()
        proyecciones_hab = []
        for proyeccion in proyecciones:
            pelicula = Pelicula.objects.get(id=proyeccion.pelicula.pk, )
            if pelicula.estado and pelicula.fechaFin > fecha_obj >= pelicula.fechaComienzo:
                proyecciones_hab.append(proyeccion)
        proyecciones_serializer = ProyeccionSerializer(proyecciones_hab, many=True)
        return JsonResponse(proyecciones_serializer.data, safe=False, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'PUT'])
def proyeccion_datail(request, pk):
    try:
        proyeccion = Proyeccion.objects.get(pk=pk)

        if request.method == 'GET':
            proyeccion_serializer = ProyeccionSerializer(proyeccion)
            return JsonResponse(proyeccion_serializer.data, safe=False, status=status.HTTP_200_OK)

        elif request.method == 'PUT':
            proyeccion_data = JSONParser().parse(request)
            proyeccion_serializer = ProyeccionSerializer(proyeccion, data=proyeccion_data)
            if proyeccion_serializer.is_valid():
                proyeccion_serializer.save()
                return JsonResponse(proyeccion_serializer.data)

    except Proyeccion.DoesNotExist:
        return JsonResponse({'Mensaje': 'La Proyeccion no existe'}, status=status.HTTP_404_NOT_FOUND)


# get proyeccion + fecha
@api_view(['GET'])
def proyeccion_datail_date(request, pk):
    proyeccion = Proyeccion.objects.get(pk=pk)

    if request.method == 'GET':
        proyeccion_serializer = ProyeccionSerializer(proyeccion)
        return JsonResponse(proyeccion_serializer.data, safe=False, status=status.HTTP_200_OK)


# Butacas
@api_view(['GET'])
def butacas_list(request):
    if request.method == 'GET':  # todas con el listado de las butacas
        butacas = Proyeccion.objects.all()
        butacas_serializer = ButacaSerializer(butacas, many=True)
        return JsonResponse(butacas_serializer.data, safe=False, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'PUT'])
def butaca_datail(request, pk):
    try:
        butaca = Butaca.objects.get(pk=pk)

        if request.method == 'GET':
            butaca_serializer = ButacaSerializer(butaca)
            return JsonResponse(butaca_serializer.data, safe=False, status=status.HTTP_200_OK)

        elif request.method == 'POST':
            butaca_data = JSONParser().parse(request)
            butaca_serializer = ButacaSerializer(data=butaca_data)
            if butaca_serializer.is_valid():
                butaca_serializer.save()
                return JsonResponse(butaca_serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == 'PUT':
            butaca_data = JSONParser().parse(request)
            butaca_serializer = ButacaSerializer(butaca, data=butaca_data)
            if butaca_serializer.is_valid():
                butaca_serializer.save()
                return JsonResponse(butaca_serializer.data)

    except Butaca.DoesNotExist:
        return JsonResponse({'Mensaje': 'La Butaca no existe'}, status=status.HTTP_404_NOT_FOUND)
