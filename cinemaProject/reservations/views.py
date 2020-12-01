from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import Pelicula
from .serializers import PeliculaSerializer
from rest_framework.decorators import api_view


@api_view(['GET', 'POST'])
def peliculas_list(request):

    if request.method == 'GET':
        peliculas = Pelicula.objects.all()
        peliculas_serializer = PeliculaSerializer(peliculas, many = True)
        return JsonResponse(peliculas_serializer.data, safe = False)

    elif request.method == 'POST':
        pelicula_data = JSONParser().parse(request)
        pelicula_serializer = PeliculaSerializer(data=pelicula_data)
        if pelicula_serializer.is_valid():
            pelicula_serializer.save()
            return JsonResponse(pelicula_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(pelicula_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
