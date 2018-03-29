# -*- coding: utf-8 -*-

from Nodo import Nodo

def crear_rama(linea, n_actual, d_nodos):
    linea = linea.split(",")
    tiempo  = float(linea[0])
    informacion=tuple(linea[1:])
    #print(informacion)
    #inp=input(">")
    n_nuevo = Nodo(tiempo, informacion)  # creacion del nodo nuevo
    id_nodo = informacion
    if id_nodo in d_nodos:  # busqueda de nodo existente
        n_existente = d_nodos[id_nodo]
        t_registrado=n_existente.getTiempo()
        t_actual=n_nuevo.getTiempo()
        if t_actual>t_registrado and t_actual<1:
            n_existente.setTiempo(t_actual)
        n_actual.siguiente_nodo(n_existente)  # enlace de nodo existete
        n_actual = n_existente

        n_actual=extraccion_secuencia(n_actual, d_nodos)
    else:
        d_nodos[id_nodo] = n_nuevo
        n_actual.siguiente_nodo(n_nuevo)  # enlace de nodo nuevo
        n_actual = n_nuevo
    return n_actual


def extraccion_secuencia(n_actual,d_nodos):
    global conteoMax, l_secuencias, secuencia
    n_actual.cuenta()  # Al existir el nodo, se lleva un conteo de las veces que ha sido usado
    # print(n_actual.getCuenta())
    if n_actual.getCuenta() >= conteoMax:
        conteoMax = n_actual.getCuenta()  # actualizacion del conteoMaximo

    # extraccion de la secuencia
    if ((100 * 0.7) <= n_actual.getCuenta()) and (secuencia.count(n_actual) == 0) and (conteoMax >= 100):
        secuencia.append(n_actual)
    else:
        if not (tuple(secuencia) in l_secuencias):
            l_secuencias.append(tuple(secuencia))
            nodo=Nodo(0.0,tuple(secuencia))
            d_nodos[tuple(secuencia)]=nodo
            secuencia = []
        else:
            nodo=d_nodos[tuple(secuencia)]
            nodo.cuenta()

            if ((100 * 0.7) <= nodo.getCuenta()) and len(secuencia)>1:
                secuencia=[nodo]
            else:
                secuencia = []
            return nodo
    return n_actual

def excava_nodo(nodo):
    info=nodo.getInformacion()
    for i in info:
        if type(i)==Nodo:
            print(i.getInformacion())
            print(i.getCuenta())
            print("++++++++++++++++++")
            excava_nodo(i)
        else:
            return 0

def main():
    nombre_archivo="lista_acciones.txt"
    n_raiz=Nodo(0,0)    #Creacion del nodo Raiz
    n_actual=n_raiz
    d_nodos={"root":n_raiz}          #creacion de diccionario de nodos
    global secuencia
    secuencia=[]   #Lista con la secuencia de elementos
    global conteoMax
    conteoMax=0     #la mayor cantidad de veces que se ha visitado un
    global l_secuencias
    l_secuencias=[]
    t_uso=0

    archivo = open(nombre_archivo, "r")     #lectura del archivo
    #print(len(archivo.readlines()))
    for linea in archivo.readlines():
        if linea.count("...")>=1:
            #print (linea.split(" ")[1])
            t_uso+=float(linea.split(" ")[1])
        else:
            if len(linea)>2 and len(linea.split(","))>2:
                #print(linea)
                n_actual=crear_rama(linea, n_actual, d_nodos)

    archivo.close()

    #Se confirman la secuencias obtenidas
    print("tiempo de uso = ", t_uso)
    print("numero de nodos = ", len(d_nodos))
    print("ConteoMax = ", conteoMax)
    print("Numero de secuencias = ", len(l_secuencias))
    print("Lista de Nodos: \n")
    #print(d_nodos)
    for s in l_secuencias:
        print (list(s))
        for e in s:
            print(e.getInformacion())
            print(e.getCuenta())
            excava_nodo(e)
            print ("---------")
        print("")

main()