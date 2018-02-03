from datetime import datetime

def actualizar_dia():
    fecha=datetime.now().day
    n_archivo="C:\Capturador\log.txt"
    archivo=open(n_archivo,"w")
    archivo.write(str(fecha))
    archivo.close()

def reiniciar_dia():
    n_archivo="C:\Capturador\log.txt"
    archivo=open(n_archivo,"w")
    archivo.write("0")
    archivo.close()

def enviar():
    try:
        n_archivo="C:\Capturador\log.txt"
        archivo=open(n_archivo,"r")
        linea=archivo.readline()
        archivo.close()

        fecha = datetime.now().day
        if int(linea) == int(fecha):
            return False
        else:
            return True

    except:
        print(Exception.with_traceback())
        actualizar_dia()
        return False

enviar()