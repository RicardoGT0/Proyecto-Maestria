# -*- coding: utf-8 -*-

from Nodo import Nodo

def crear_rama(linea, n_actual, d_nodos):
    linea = linea.split(",")
    dispositivo = linea[0]
    accion = linea[1]
    tiempo = float(linea[2])
    if len(linea) >= 5:
        colocacion = []
        colocacion.append(int(linea[3]))
        colocacion.append(int(linea[4]))
        colocacion = tuple(colocacion)
    else:
        colocacion = str(linea[3])[:-1]
    n_nuevo = Nodo(dispositivo, accion, tiempo, colocacion)  # creacion del nodo nuevo
    id_nodo = str(accion) + str(colocacion)
    if id_nodo in d_nodos:  # busqueda de nodo existente
        n_existente = d_nodos[id_nodo]
        t_registrado=n_existente.getTiempo()
        t_actual=n_nuevo.getTiempo()
        if t_actual>t_registrado and t_actual<1:
            n_existente.setTiempo(t_actual)
        n_actual.siguiente_nodo(n_existente)  # enlace de nodo existete
        n_actual = n_existente

        extraccion_secuencia(n_actual)
    else:
        d_nodos[id_nodo] = n_nuevo
        n_actual.siguiente_nodo(n_nuevo)  # enlace de nodo nuevo
        n_actual = n_nuevo
    return n_actual


def extraccion_secuencia(n_actual):
    global conteoMax, l_secuencias, secuencia
    n_actual.cuenta()  # Al existir el nodo, se lleva un conteo de las veces que ha sido usado
    # print(n_actual.getCuenta())
    if n_actual.getCuenta() >= conteoMax:
        conteoMax = n_actual.getCuenta()  # actualizacion del conteoMaximo

    # extraccion de la secuencia
    if ((conteoMax * 0.75) <= n_actual.getCuenta()) and (secuencia.count(n_actual) == 0) and (conteoMax >= 100):
        secuencia.append(n_actual)
    else:
        if not (secuencia in l_secuencias) and secuencia:
            l_secuencias.append(secuencia)
        secuencia = []

def main():
    nombre_archivo="lista_acciones.txt"
    n_raiz=Nodo(0,0,0,0)    #Creacion del nodo Raiz
    n_actual=n_raiz
    d_nodos={"root":n_raiz}          #creacion de diccionario de nodos
    global secuencia
    secuencia=[]   #Lista con la secuencia de elementos
    global conteoMax
    conteoMax=0     #la mayor cantidad de veces que se ha visitado un
    global l_secuencias
    l_secuencias=[]

    archivo = open(nombre_archivo, "r")     #lectura del archivo
    for linea in archivo.readlines():
        if len(linea)>2:
            n_actual=crear_rama(linea, n_actual, d_nodos)

    archivo.close()

    #Se confirman la secuencias obtenidas
    """
    print(len(d_nodos))
    for s in l_secuencias:
        print (s)
        for e in s:
            print (e.getDispositivo()+e.getAccion()+e.getColocacion())
        print("")
    """

main()