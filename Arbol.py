# -*- coding: utf-8 -*-

from Nodo import Nodo

nombre_archivo="prueba.txt"
n_raiz=Nodo(0,0,0,0)    #Creacion del nodo Raiz
n_actual=n_raiz
d_nodos={}          #creacion de diccionario de nodos

archivo = open(nombre_archivo, "r")     #lectura del archivo
for linea in archivo.readlines():
    linea=linea.split(",")
    dispositivo = linea[0]
    accion=linea[1]
    tiempo=int(linea[2])
    if len(linea)>=5:
        colocacion=[]
        colocacion.append(int(linea[3]))
        colocacion.append(int(linea[4]))
        colocacion=tuple(colocacion)
    else:
        colocacion=str(linea[3])[:-1]

    n_nuevo = Nodo(dispositivo, accion, tiempo, colocacion) #creacion del nodo nuevo

    id_nodo=str(accion)+str(colocacion)
    if id_nodo in d_nodos:  #busqueda de nodo existente
        n_existente=d_nodos[id_nodo]
        n_actual.siguiente_nodo( n_existente)  # enlace de nodo existete
        n_actual=n_existente
        n_actual.cuenta()
    else:
        d_nodos[id_nodo]=n_nuevo
        n_actual.siguiente_nodo(n_nuevo)    # enlace de nodo nuevo
        n_actual=n_nuevo

archivo.close()
