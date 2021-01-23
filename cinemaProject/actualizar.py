import os
from time import sleep
import datetime

hora_de_ejecucion = "7:00"

while True:
    hora_actual = datetime.datetime.now().strftime("%H:%M")
    if hora_actual == hora_de_ejecucion:
        os.system("python3 manage.py runscript service")
        sleep(1380)
    else:
        sleep(30)
