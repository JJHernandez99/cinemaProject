from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import Pelicula, Sala, Butaca, Proyeccion
from .serializers import PeliculaSerializer, SalaSerializer, ButacaSerializer, ProyeccionSerializer
from rest_framework.decorators import api_view


@api_view(['GET', 'POST'])
def peliculas_list(request):

    if request.method == 'GET':
        peliculas = Pelicula.objects.all()
        peliculas_serializer = PeliculaSerializer(peliculas, many = True)
        return JsonResponse(peliculas_serializer.data, safe = False, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        pelicula_data = JSONParser().parse(request)
        pelicula_serializer = PeliculaSerializer(data=pelicula_data)
        if pelicula_serializer.is_valid():
            pelicula_serializer.save()
            return JsonResponse(pelicula_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(pelicula_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def salas_list(request):

    if request.method == 'GET':
        salas = Sala.objects.all()
        salas_serializer = SalaSerializer(salas, many = True)
        return JsonResponse(salas_serializer.data, safe = False, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        salas_data = JSONParser().parse(request)
        salas_serializer = SalaSerializer(data=salas_data)
        if salas_serializer.is_valid():
            salas_serializer.save()
            return JsonResponse(salas_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(salas_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def sala_detail(request,pk):

    try:
        sala = Sala.objects.get(pk=pk)

        if request.method == 'GET':
            sala_serializer = SalaSerializer(sala)
            return JsonResponse(sala_serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'PUT':
            sala_data = JSONParser().parse(request)
            sala_serializer = SalaSerializer(sala, data= sala_data)
            if sala_serializer.is_valid():
                sala_serializer.save()
                return JsonResponse(sala_serializer.data)
            return JsonResponse(sala_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            sala.delete()
            return JsonResponse({'Mensaje' : 'La sala se elimino correctamente'},status=status.HTTP_204_NO_CONTENT)

    except Sala.DoesNotExist:
        return JsonResponse({'Mensaje' : 'La sala no existe'},status=status.HTTP_404_NOT_FOUND)

