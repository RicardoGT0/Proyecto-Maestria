import datetime

def actualizar_mes():
    fecha=datetime.datetime.now()
    n_archivo="log.txt"
    archivo=open(n_archivo,"w")
    archivo.write(str(fecha.month))
    archivo.close()

def enviar():
    try:
        n_archivo="log.txt"
        archivo=open(n_archivo,"r")
        linea=archivo.readline()
        archivo.close()

        if int(linea)<int(datetime.datetime.now().month):
            return True
        else:
            return False
    except:
        actualizar_mes()
        return False