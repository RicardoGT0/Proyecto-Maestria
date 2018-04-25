from pynput import mouse, keyboard
from threading import Thread
import time, sys
from os import remove
from Nodo import Nodo

n_raiz = Nodo(0, 0)  # Creacion del nodo Raiz
n_actual = n_raiz
d_nodos = {"root": n_raiz}  # creacion de diccionario de nodos
secuencia = []  # Lista con la secuencia de elementos
conteoMax = 0  # la mayor cantidad de veces que se ha visitado un
d_secuencias = {}
l_ignoradas = []
l_secuencias = []
t_inicial = time.time()
lista = []


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
        # extraccion de la secuencia
        if (conteoMax >= 100 and bandera == 0):
            extraccion_secuencia()
    else:
        d_nodos[id_nodo] = n_nuevo
        n_actual.siguiente_nodo(n_nuevo)  # enlace de nodo nuevo
        n_actual = n_nuevo


def extraccion_secuencia():
    global conteoMax, l_secuencias, secuencia, d_secuencias, l_ignoradas

    # print("conteo del nodo: ", n_actual.getCuenta())
    # print("Conteo Max: ", conteoMax)

    if ((100 * 0.7) < n_actual.getCuenta()) and (not (n_actual in secuencia)):
        secuencia.append(n_actual)  # creacion de la secuencia
    else:
        # Almacenar la secuencia
        if (not (secuencia in l_secuencias)) and len(secuencia) > 1 and (not (secuencia in l_ignoradas)):

            print(secuencia)
            for e in secuencia:
                print(e.getInformacion())

            print("Que haces?(i)gnorar  (Escribe el nombre para guardar)")
            inp = str(input(">>"))

            if inp != "i":
                l_secuencias.append(secuencia)
                d_secuencias[inp] = secuencia
            else:
                l_ignoradas.append(secuencia)
        secuencia = []


def carga(nombre_archivo):
    global l_ignoradas, l_secuencias, d_secuencias
    archivo = open("C:\Capturador" + nombre_archivo + ".txt", "r")  # lectura del archivo
    # print(len(archivo.readlines()))
    llave = ""
    secuencia = []

    for linea in archivo.readlines():
        if linea.count("--") >= 1:
            if nombre_archivo == "\l_secuencias" and len(secuencia) > 0:
                d_secuencias[llave] = [secuencia]
                l_secuencias.append(secuencia)
            if nombre_archivo == "\l_ignoradas" and len(secuencia) > 0:
                l_ignoradas.append(secuencia)

            llave = linea[3:]
            secuencia = []
        else:
            if len(linea) > 2 and len(linea.split(",")) > 2:
                if nombre_archivo == "\l_acciones":
                    linea = linea.split(",")
                    crear_rama(linea=linea, bandera=1)

                else:
                    informacion = tuple(linea.split(","))
                    nodo = d_nodos[informacion]
                    secuencia.append(nodo)
    if nombre_archivo == "\l_secuencias" and len(secuencia) > 0:
        d_secuencias[llave] = secuencia
        l_secuencias.append(secuencia)
    if nombre_archivo == "\l_ignoradas" and len(secuencia) > 0:
        l_ignoradas.append(secuencia)

    archivo.close()


def respaldo():
    while True:
        time.sleep(10)
        try:
            remove("C:\Capturador\l_secuencias.txt")
        except:
            pass
        try:
            remove("C:\Capturador\l_ignoradas.txt")
        except:
            pass
        llaves = d_secuencias.keys()

        for llave in llaves:
            print(llave)
            escribir_accion(["--", llave], "\l_secuencias")
            secuencia = d_secuencias[llave]
            print(d_secuencias)
            for accion in secuencia:
                escribir_accion(accion.getInformacion(), "\l_secuencias")

        for secuencia in l_ignoradas:
            print(secuencia)
            escribir_accion(["--"], "\l_ignoradas")
            for accion in secuencia:
                escribir_accion(accion.getInformacion(), "\l_ignoradas")
        time.sleep(30)


def escribir_accion(accion, archivo):
    # Escribe tuplas o listas en el archivo especificado en un formato de valores separados por comas
    n_archivo = "C:\Capturador" + archivo + ".txt"
    archivo = open(n_archivo, "a")
    cadena = ""
    for elemento in accion:
        cadena += str(elemento) + ","
    archivo.write(cadena[:-1] + "\n")
    archivo.close()


def procesamiento():
    global lista
    while True:
        print(len(lista))
        for elemento in lista:
            crear_rama(elemento, 0)
            escribir_accion(elemento, "\l_acciones")
        lista = []
        time.sleep(5)


def tiempo(t_final):
    global lista
    global t_inicial
    t_total = round(t_final - t_inicial, 2)
    t_inicial = time.time()
    return t_total


def on_move(x, y):
    global lista
    colocacion = ('{0},{1}'.format(x, y))
    lista.append((tiempo(time.time()), "Mouse", "Moved", colocacion))


def on_click(x, y, button, pressed):
    global lista
    accion = "{0}".format('Pressed' if pressed else 'Released')
    lista.append((tiempo(time.time()), "Mouse", accion, str(button)))


def on_scroll(x, y, dx, dy):
    global lista
    colocacion = ('{0}'.format('Down' if dy < 0 else 'Up'))
    lista.append((tiempo(time.time()), "Mouse", "Scrolled", colocacion))


def on_press(key):
    global lista
    try:
        lista.append((tiempo(time.time()), "Keyboard", "Pressed", key.char))
    except AttributeError:
        lista.append((tiempo(time.time()), "Keyboard", "Pressed", str(key)))
    except TypeError:
        pass


def on_release(key):
    global lista
    try:
        lista.append((tiempo(time.time()), "Keyboard", "Release", key.char))
    except AttributeError:
        lista.append((tiempo(time.time()), "Keyboard", "Release", str(key)))
    except TypeError:
        pass


try:
    carga("\l_acciones")
except:
    print(sys.exc_info()[1])
try:
    carga("\l_secuencias")
except:
    print(sys.exc_info()[1])
try:
    carga("\l_ignoradas")
except:
    print(sys.exc_info()[1])

listener_keyboard = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)

listener_mouse = mouse.Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll)

proc = Thread(target=procesamiento)
resp = Thread(target=respaldo)

proc.start()
resp.start()
listener_keyboard.start()
listener_mouse.start()
