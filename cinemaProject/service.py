import requests
import pymysql.cursors
import datetime as dt

#Acceso al servicio web de peliculas
r = requests.get('http://localhost:5000/api/pelicula/')
peliculas_servicio = r.json()

#Conexión a la base de datos
print("Conectando a la base de datos ...")
try:
    conn = pymysql.connect(host='54.207.134.40',
                           user='root',
                           password='12345678',
                           db='cineTestingDB',
                           cursorclass=pymysql.cursors.DictCursor)
    print("Conexion exitosa")
except:
    print("No se puede conectar a la base de datos")
    exit()

#Adecuacion de parametros del servicio a nuestra bd
for pelicula in peliculas_servicio:
    pelicula['fechaComienzo']=dt.datetime.strptime(pelicula['fechaComienzo'],'%Y-%m-%dT%H:%M:%S+%f').date()
    pelicula['fechaFinalizacion'] = dt.datetime.strptime(pelicula['fechaFinalizacion'],'%Y-%m-%dT%H:%M:%S+%f').date()
    if(pelicula['estado']=="Activa"):
        pelicula['estado']=1
    else:
        pelicula['estado']=0

# with conn.cursor() as cursor:
#     try:
#
#         sql ="Select * from reservations_pelicula"
#
#        # Execute the SQL command
#         cursor.execute(sql)
#         print()
#        # Fetch all the rows in a list of lists.
#         for row in cursor:
#             print(row)
#
#     finally:
#         conn.close()

pelicula=peliculas_servicio[0]

with conn.cursor() as cursor:
    sql = (f"INSERT INTO reservations_pelicula (nombre, duracion, descripcion, detalle, genero, clasificacion, estado, fechaComienzo,\
                    FechaFin) "
           f"VALUES (%({')s, %('.join(pelicula.keys())})s)")
    try:
        cursor.execute(sql, pelicula)
        conn.commit()
    except Exception as e:
        print("Exeception occured:{}".format(e))
    finally:
        conn.close()
