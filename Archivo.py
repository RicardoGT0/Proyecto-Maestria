from time import time

t_inicial=time()

def escribir(dispositivo, accion, t_final, colocacion):
    global t_inicial
    n_archivo="C:\Capturador\lista_acciones.txt"
    archivo=open(n_archivo,"a")
    tiempo=round(t_final-t_inicial,2)
    archivo.write(dispositivo + "," + accion + "," + str(tiempo) + "," + colocacion + "\n")
    archivo.close()
    t_inicial = time()