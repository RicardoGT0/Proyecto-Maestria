import time, sys
from Nodo import Nodo
from Grafo import GraphClass
from _graph.GraphPro import GraphPro


n_raiz = Nodo(0, 0)  # Creacion del nodo Raiz
n_actual = n_raiz
d_nodos = {"root": n_raiz}  # creacion de diccionario de nodos
secuencia = []  # Lista con la secuencia de elementos
conteoMax = 0  # la mayor cantidad de veces que se ha visitado un
d_secuencias = {}
l_ignoradas = []
l_secuencias = []
l_conteo=[]
t_inicial = time.time()
lista = []
conteo_tareas=0
inp=0

def crear_rama(linea, bandera):
    global conteoMax, n_actual
    tiempo = float(linea[0])
    informacion = tuple(linea[1:])
    n_nuevo = Nodo(tiempo, informacion)  # creacion del nodo nuevo
    id_nodo = informacion

    if id_nodo in d_nodos:  # busqueda de nodo existente
        n_existente = d_nodos[id_nodo]
        t_registrado = n_existente.getTiempo()
        t_actual = n_nuevo.getTiempo()
        if t_actual > t_registrado and t_actual < 1:
            n_existente.setTiempo(t_actual)
        n_actual.siguiente_nodo(n_existente)  # enlace de nodo existete
        n_actual = n_existente

        n_actual.cuenta()  # Al existir el nodo, se lleva un conteo de las veces que ha sido usado
        if n_actual.getCuenta() >= conteoMax:
            conteoMax = n_actual.getCuenta()  # actualizacion del conteoMaximo
    else:
        d_nodos[id_nodo] = n_nuevo
        n_actual.siguiente_nodo(n_nuevo)  # enlace de nodo nuevo
        n_actual = n_nuevo


def carga(nombre_archivo):
    global l_ignoradas, l_secuencias, d_secuencias, l_conteo
    archivo = open(nombre_archivo + ".txt", "r")  # lectura del archivo
    # print(len(archivo.readlines()))
    llave = ""
    secuencia = []

    for linea in archivo.readlines():
        if len(linea) > 2 and len(linea.split(",")) > 2:
            #crear arbol a partir del respaldo
            linea = linea.split(",")
            linea[-1]=linea[-1][:-1]#eliminar salto de linea de la cadena

            if (linea[1] == "Keyboard") and len(d_nodos)<=150:
            #if (linea[1] == "Mouse") and len(d_nodos) <= 600:
                crear_rama(linea=linea, bandera=0)  #Bandera=1 es para no preguntar al cargar el respaldo
    archivo.close()


#Carga de respaldo en disco
try:
    print("carga", "compiladoN")
    carga("compiladoN")
    print("Datos Cargados")
except:
    print(sys.exc_info()[1])


Nodos=list(d_nodos.keys()) #obteniendo la lista de nodos por nombre
"""
# inicializando la matriz de distancias para el grafo
n=len(Nodos)
Matriz=[]
c=0
print("N= ",n)
for i in range(n):
    Matriz.append([0]*n)
    c+=1

#obteniendo relaciones de los demas nodos
c=0
for llave in d_nodos:
    nodo=d_nodos[llave]
    l_siguiente=nodo.getSiguiente_nodo()
    for e in l_siguiente:
        i = Nodos.index(e.getInformacion())
        Matriz[c][i] += 1
    c+=1

#usando graphviz
g=GraphClass(Nodos, Matriz)
g.draw()


"""
sources=[]
targets=[]
weights=[]
#obteniendo relaciones de los demas nodos
c=0
for llave in d_nodos:
    nodo=d_nodos[llave]
    l_siguiente=nodo.getSiguiente_nodo()
    for e in l_siguiente:
        i = Nodos.index(e.getInformacion())
        sources.append(c)
        targets.append(i)
        weights.append(1)
    c+=1

graph = GraphPro(sources, targets, weights)
graph.draw()
