from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import Pelicula, Sala, Butaca, Proyeccion
from .serializers import PeliculaSerializer, SalaSerializer, ButacaSerializer, ProyeccionSerializer
from rest_framework.decorators import api_view
import datetime as dt


# Peliculas
@api_view(['GET'])
def peliculas_list(request):
    if request.method == 'GET':
        # Devuelve peliculas con fecha valida en rango 10 dias antes y despues de la fecha actual
        fecha_actual = dt.datetime.now()
        ventana_tiempo = dt.timedelta(days=15)
        peliculas = Pelicula.objects.filter(fechaFinalizacion__gte=(fecha_actual - ventana_tiempo),
        fechaComienzo__lte=(fecha_actual + ventana_tiempo))
        peliculas_serializer = PeliculaSerializer(peliculas, many=True)
        return JsonResponse(peliculas_serializer.data, safe=False, status=status.HTTP_200_OK)

    # elif request.method == 'POST':
    #     pelicula_data = JSONParser().parse(request)
    #     pelicula_serializer = PeliculaSerializer(data=pelicula_data)
    #     if pelicula_serializer.is_valid():
    #         pelicula_serializer.save()
    #         return JsonResponse(pelicula_serializer.data, status=status.HTTP_201_CREATED)
    #     return JsonResponse(pelicula_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Get pelicula + fecha
#http://127.0.0.1:8000/api/peliculas/9/21-12-2020/25-12-2020
@api_view(['GET'])
def pelicula_detail(request, pk, fechaI, fechaF):
    try:
        pelicula = Pelicula.objects.get(pk=pk)

        if request.method == 'GET':
            pelicula_serializer = PeliculaSerializer(pelicula)
            respuesta = []
            fechaI = dt.datetime.strptime(fechaI, '%d-%m-%Y').date()
            fechaF = dt.datetime.strptime(fechaF, '%d-%m-%Y').date()
            proyecciones = Proyeccion.objects.filter(pelicula=pelicula, fechaFin__gte=fechaI, fechaInicio__lte=fechaF)
            if proyecciones.count() != 0:
                respuesta.append({
                    'Pelicula': pelicula.nombre
                }
                )
                fechas = []
                c = 0
                for proyeccion in proyecciones:
                    fecha_actual = max(fechaI, proyeccion.fechaInicio)
                    fechas.append([])
                    while (fecha_actual <= fechaF and fecha_actual <= proyeccion.fechaFin):
                        fechas[c].append(fecha_actual)
                        fecha_actual += dt.timedelta(days=1)
                    respuesta.append({
                        'Proyeccion': proyeccion.id,
                        'Sala': proyeccion.sala.nombre,
                        'Fechas proyeccion': '{} al {}'.format(proyeccion.fechaInicio, proyeccion.fechaFin),
                        'Fechas Disponibles': fechas[c]
                    })
                    c += 1
                return JsonResponse(respuesta, safe=False, status=status.HTTP_200_OK)
            return JsonResponse({'Mensaje': 'No existen proyecciones de la pelicula en las fechas deseadas'},
                                status=status.HTTP_404_NOT_FOUND)

    except Pelicula.DoesNotExist:
        return JsonResponse({'Mensaje': 'La pelicula especificada no existe'}, status=status.HTTP_404_NOT_FOUND)


# @api_view(['DELETE'])
# def pelicula_delete(request, pk):
#     try:
#         pelicula = Pelicula.objects.get(pk=pk)
#         if request.method == 'DELETE':
#             pelicula.delete()
#             return JsonResponse({'Mensaje': 'La pelicula se elimino correctamente'}, status=status.HTTP_204_NO_CONTENT)
#
#     except Pelicula.DoesNotExist:
#         return JsonResponse({'Mensaje': 'La pelicula especificada no existe'}, status=status.HTTP_404_NOT_FOUND)


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
                proyecciones = Proyeccion.objects.filter(sala=sala)
                if (proyecciones.count() != 0):
                    for proyeccion in proyecciones:
                        if (proyeccion.estado):
                            return JsonResponse({'Mensaje':
                                                     'Sala asociada, deshabilite la proyeccion para editar la sala'})
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

#http://127.0.0.1:8000/api/proyecciones/22-12-2020
@api_view(['GET'])
def proyecciones_list_range(request, fecha):
    fecha_obj = dt.datetime.strptime(fecha, '%d-%m-%Y').date()
    if request.method == 'GET':
        proyecciones = Proyeccion.objects.filter(fechaInicio__lte=fecha_obj, fechaFin__gte=fecha_obj,
                                                 estado__exact=True)
        proyecciones_serializer = ProyeccionSerializer(proyecciones, many=True)
        return JsonResponse(proyecciones_serializer.data, safe=False, status=status.HTTP_200_OK)

#http://127.0.0.1:8000/api/proyecciones/10/16-11-2020
@api_view(['GET'])
def proyeccion_detail_range(request, pk, fecha):
    fecha_obj = dt.datetime.strptime(fecha, '%d-%m-%Y').date()
    try:
        proyeccion = Proyeccion.objects.get(pk=pk)

        if request.method == 'GET':
            pelicula_serializer = PeliculaSerializer(proyeccion.pelicula)
            sala_serializer = SalaSerializer(proyeccion.sala)
            butacas = Butaca.objects.filter(proyeccion=proyeccion, fecha=fecha_obj)

            butacas_posiciones = {}
            id = 0
            for fila in range(proyeccion.sala.fila):
                for asiento in range(proyeccion.sala.asiento):
                    for butaca in butacas:
                        if ((butaca.fila - 1) == fila):
                            if ((butaca.asiento - 1) == asiento):
                                butacas_posiciones[id] = {
                                    'fila': butaca.fila,
                                    'asiento': butaca.asiento,
                                    'estado': 'Reservada',
                                }
                    try:
                        butacas_posiciones[id]
                    except:
                        butacas_posiciones[id] = {
                            'fila': fila + 1,
                            'asiento': asiento + 1,
                            'estado': 'Libre',
                        }
                    finally:
                        id += 1

            respuesta = {
                'Pelicula': pelicula_serializer.data,
                'Sala': sala_serializer.data,
                'Butacas': butacas_posiciones
            }

            return JsonResponse(respuesta, safe=False, status=status.HTTP_200_OK)

    except Proyeccion.DoesNotExist:
        return JsonResponse({'Mensaje': 'La Proyeccion no existe'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def proyeccion_detail(request, pk, ):
    try:
        proyeccion = Proyeccion.objects.get(pk=pk)

        # if request.method == 'GET':
        #     proyeccion_serializer = ProyeccionSerializer(proyeccion)
        #     return JsonResponse(proyeccion_serializer.data, status=status.HTTP_200_OK)

        if request.method == 'PUT':
            proyeccion_data = JSONParser().parse(request)
            proyeccion_serializer = ProyeccionSerializer(proyeccion, data=proyeccion_data)
            if proyeccion_serializer.is_valid():
                return corroborar_proyeccion(proyeccion_data, proyeccion_serializer, proyeccion)
            return JsonResponse(proyeccion_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Proyeccion.DoesNotExist:
        return JsonResponse({'Mensaje': 'La Proyeccion no existe'}, status=status.HTTP_404_NOT_FOUND)


def corroborar_proyeccion(proyeccion_data, proyeccion_serializer, proyeccion_orig=None):
    # Solo creo proyeccion si la peli esta hab , las fechas son validas, y la sala no esta deshab ni ocupada
    pelicula = Pelicula.objects.get(pk=proyeccion_data['pelicula'])
    sala = Sala.objects.get(pk=proyeccion_data['sala'])
    proyecciones = Proyeccion.objects.filter(sala=sala)
    fecha_inicio = dt.datetime.strptime(proyeccion_data['fechaInicio'], '%Y-%m-%d').date()
    fecha_fin = dt.datetime.strptime(proyeccion_data['fechaFin'], '%Y-%m-%d').date()
    if pelicula.estado:
        if sala.estado:
            if (pelicula.fechaComienzo <= fecha_inicio and
                    pelicula.fechaFinalizacion >= fecha_fin):
                for proyeccion in proyecciones:
                    if not (proyeccion == proyeccion_orig):
                        if proyeccion.fechaInicio < fecha_inicio and proyeccion.fechaFin < fecha_inicio:
                            pass
                        elif proyeccion.fechaInicio > fecha_fin and proyeccion.fechaFin > fecha_fin:
                            pass
                        else:
                            return JsonResponse({'Mensaje': 'Sala ya ocupada en esas fechas'},
                                                status=status.HTTP_400_BAD_REQUEST)
                proyeccion_serializer.save()
                return JsonResponse(proyeccion_serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse({'Mensaje': 'Fecha invalida para la pelicula seleccionada'},
                                status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'Mensaje': 'La sala esta deshabilitada'},
                            status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'Mensaje': 'La pelicula esta deshabilitada'},
                        status=status.HTTP_400_BAD_REQUEST)


# Butacas
@api_view(['GET', 'POST', 'DELETE'])
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
    fecha = dt.datetime.strptime(butaca_data['fecha'], '%Y-%m-%d').date()
    if proyeccion.estado:
        sala = proyeccion.sala
        if (fecha <= proyeccion.fechaFin and fecha >= proyeccion.fechaInicio):
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
        return JsonResponse({'Mensaje': 'La fecha seleccionada es invalida para la proyeccion'},
                            status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'Mensaje': 'La proyeccion especificada esta inhabilitada para reservas'},
                        status=status.HTTP_400_BAD_REQUEST)

#http://localhost:8000/api/reportes/butacas/20-07-2021/20-08-2021
@api_view(['GET'])
def reporte_butacas(request, fechaI, fechaF):
    if request.method == 'GET':
        fechaI = dt.datetime.strptime(fechaI, '%d-%m-%Y').date()
        fechaF = dt.datetime.strptime(fechaF, '%d-%m-%Y').date()

        butacas = Butaca.objects.filter(fecha__gte=fechaI, fecha__lte=fechaF)
        cantidad_butacas = butacas.count()
        respuesta = {
            'Rango de fecha': '{} al {}'.format(fechaI, fechaF),
            'Cantidad de butacas vendidas en el periodo': cantidad_butacas
        }
        return JsonResponse(respuesta, status=status.HTTP_200_OK)

#http://localhost:8000/api/reportes/butacas/2/20-07-2021/20-08-2021
@api_view(['GET'])
def reporte_butacas_proyeccion(request, pk, fechaI, fechaF):
    try:
        proyeccion = Proyeccion.objects.get(pk=pk)

        if request.method == 'GET':
            fechaI = dt.datetime.strptime(fechaI, '%d-%m-%Y').date()
            fechaF = dt.datetime.strptime(fechaF, '%d-%m-%Y').date()

            butacas = Butaca.objects.filter(fecha__gte=fechaI, fecha__lte=fechaF, proyeccion=proyeccion)
            cantidad_butacas = butacas.count()
            respuesta = {
                'Rango de fecha': '{} al {}'.format(fechaI, fechaF),
                'Proyeccion': proyeccion.id,
                'Pelicula': proyeccion.pelicula.nombre,
                'Sala': proyeccion.sala.nombre,
                'Cantidad de butacas vendidas para la proyeccion en el periodo': cantidad_butacas
            }
            return JsonResponse(respuesta, status=status.HTTP_200_OK)

    except Proyeccion.DoesNotExist:
        return JsonResponse({'Mensaje': 'La Proyeccion no existe'}, status=status.HTTP_404_NOT_FOUND)

#http://localhost:8000/api/reportes/peliculas
@api_view(['GET'])
def reporte_entradas_peliculas(request):
    fecha_actual = dt.date.today()

    if request.method == 'GET':
        peliculas = Pelicula.objects.filter(estado=True)
        respuesta = []
        for pelicula in peliculas:
            total = 0
            proyecciones = Proyeccion.objects.filter(pelicula=pelicula)
            for proyeccion in proyecciones:
                butacas = Butaca.objects.filter(proyeccion=proyeccion, fecha__lte=fecha_actual)
                total += butacas.count()
            respuesta.append({
                'Pelicula': pelicula.nombre,
                'Cantidad de butacas vendidas hasta {}: '.format(fecha_actual): total,
            })

        return JsonResponse(respuesta, safe=False, status=status.HTTP_200_OK)

#http://localhost:8000/api/reportes/proyecciones/01-12-2020/30-12-2020
@api_view(['GET'])
def reporte_ranking_proyecciones(request, fechaI, fechaF):
    if request.method == 'GET':
        fechaI = dt.datetime.strptime(fechaI, '%d-%m-%Y').date()
        fechaF = dt.datetime.strptime(fechaF, '%d-%m-%Y').date()

        proyecciones = Proyeccion.objects.filter(fechaInicio__lte=fechaF, fechaFin__gte=fechaI)
        ranking = []
        for proyeccion in proyecciones:
            butacas = Butaca.objects.filter(proyeccion=proyeccion, fecha__gte=fechaI, fecha__lte=fechaF)
            vendidas = butacas.count()
            ranking.append({
                'Proyeccion': proyeccion.id,
                'Sala': proyeccion.sala.nombre,
                'Pelicula': proyeccion.pelicula.nombre,
                'Butacas vendidas': vendidas
            })
        respuesta = sorted(ranking, key=lambda k: k['Butacas vendidas'], reverse=True)
        respuesta = respuesta[:5]

        return JsonResponse(respuesta, safe=False, status=status.HTTP_200_OK)
