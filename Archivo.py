from time import time

t_inicial=time()
contador=0

def escribir_accion(t_final, dispositivo, accion, colocacion):
    global t_inicial,contador
    n_archivo="C:\Capturador\lista_acciones.txt"
    archivo=open(n_archivo,"a")
    contador=(t_final-t_inicial)+contador
    if contador>=3600:
        archivo.write("... "+str(round(contador/3600,1))+"\n")
        contador = 0
    else:
        pass
    tiempo=round(t_final-t_inicial,2)
    archivo.write( str(tiempo) + "," + dispositivo + "," + accion + "," + colocacion + "\n")
    archivo.close()
    t_inicial = time()