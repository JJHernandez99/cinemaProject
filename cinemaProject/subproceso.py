from time import sleep
from subprocess import call
import datetime

hora_de_ejecucion = "07:00"

while True:
    hora_actual = datetime.datetime.now().strftime("%H:%M")
    if hora_actual == hora_de_ejecucion:
        print("{} - Actualizando DB...".format(hora_actual))
        call(['python3', 'actualizar.py', ])
        sleep(84600)
    else:
        sleep(30)
