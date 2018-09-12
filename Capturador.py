from pynput import mouse, keyboard
from threading import Thread
import time, sys
from os import remove
from Nodo import Nodo
from tkinter import *
from PopupWindow import popupWindow

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
    global l_secuencias, secuencia, l_conteo

    # print("conteo del nodo: ", n_actual.getCuenta())
    # print("Conteo Max: ", conteoMax)

    if ((100 * 0.7) < n_actual.getCuenta()) and (not (n_actual in secuencia)):
        secuencia.append(n_actual)  # creacion de la secuencia
    else:
        # Almacenar la secuencia
        if len(secuencia) > 1 and (not (secuencia in l_ignoradas)):
            # print(secuencia)

            if (secuencia in l_secuencias):
                extraccion_tarea()
            else:
                l_secuencias.append(secuencia)
                l_conteo.append(0)
        secuencia = []


def extraccion_tarea():
    global l_secuencias, l_conteo, d_secuencias, l_ignoradas
    i = l_secuencias.index(secuencia)
    l_conteo[i] += 1

    existe = False  # verifica que la secuencia no este en el diccionario de secuencias,
    for e in d_secuencias:
        if secuencia == d_secuencias[e]:
            existe = True

    if (l_conteo[i] > 5) and (not existe):
        cadena = []
        for e in secuencia:
            cadena.append(e.getInformacion())
        popup = popupWindow(master, cadena)
        master.wait_window(popup.top)
        inp = popup.value

        if inp != "ignorar secuencia":
            d_secuencias[inp] = secuencia
            listbox1.insert(END, inp)
        else:
            l_ignoradas.append(secuencia)
            l_secuencias.remove(secuencia)


def carga(nombre_archivo):
    global l_ignoradas, l_secuencias, d_secuencias, l_conteo
    archivo = open(nombre_archivo + ".txt", "r")  # lectura del archivo
    # print(len(archivo.readlines()))
    llave = ""
    secuencia = []

    for linea in archivo.readlines():
        if linea.count("--") >= 1:
            if nombre_archivo == "l_secuencias" and len(secuencia) > 0:
                d_secuencias[llave] = secuencia
                l_secuencias.append(secuencia)
                l_conteo.append(-1)

            if nombre_archivo == "l_ignoradas" and len(secuencia) > 0:
                l_ignoradas.append(secuencia)

            llave = linea[3:-1]
            secuencia = []
        else:
            if len(linea) > 2 and len(linea.split(",")) > 2:
                if nombre_archivo == "l_acciones":
                    #crear arbol a partir del respaldo
                    linea = linea.split(",")
                    linea[-1]=linea[-1][:-1]#eliminar salto de linea de la cadena
                    crear_rama(linea=linea, bandera=0)  #Bandera=1 es para no preguntar al cargar el respaldo
                else:
                    #crear secuencia a partir del respaldo
                    informacion = linea.split(",")
                    informacion[-1]=informacion[-1][:-1]#eliminar salto de linea de la cadena
                    nodo = d_nodos[tuple(informacion)]
                    secuencia.append(nodo)

    if nombre_archivo == "l_secuencias" and len(secuencia) > 0:
        d_secuencias[llave] = secuencia
        l_secuencias.append(secuencia)
    if nombre_archivo == "l_ignoradas" and len(secuencia) > 0:
        l_ignoradas.append(secuencia)

    archivo.close()


def respaldo():

    while True:
        time.sleep(10)
        try:
            remove("l_secuencias.txt")
        except:
            pass
        try:
            remove("l_ignoradas.txt")
        except:
            pass
        llaves = d_secuencias.keys()
        print("ejecutando Respaldo", "l_secuencias")
        print(len(d_secuencias))
        for llave in llaves:
            escribir_accion(["--", llave], "l_secuencias")
            secuencia = d_secuencias[llave]
            #print(llave, secuencia)
            for accion in secuencia:
                escribir_accion(accion.getInformacion(), "l_secuencias")
        print("ejecutando Respaldo", "l_ignoradas")
        print(len(l_ignoradas))
        for secuencia in l_ignoradas:
            #print(secuencia)
            escribir_accion(["--"], "l_ignoradas")
            for accion in secuencia:
                escribir_accion(accion.getInformacion(), "l_ignoradas")
        time.sleep(30)


def escribir_accion(accion, archivo):
    # Escribe tuplas o listas en el archivo especificado en un formato de valores separados por comas
    n_archivo = archivo + ".txt"
    archivo = open(n_archivo, "a")
    cadena = ""
    for elemento in accion:
        cadena += str(elemento) + ","
    archivo.write(cadena[:-1] + "\n")
    archivo.close()


def procesamiento():
    global lista
    while True:
        #print(len(lista))
        for elemento in lista:
            crear_rama(elemento, 0)
            escribir_accion(elemento, "l_acciones") #respaldo de la accion
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

"""
#Carga de respaldo en disco
try:
    print("carga", "l_acciones")
    carga("l_acciones")
except:
    print(sys.exc_info()[1])

try:
    print("carga","l_secuencias")
    carga("\l_secuencias")
except:
    print(sys.exc_info()[1])
try:
    print("carga","l_ignoradas")
    carga("l_ignoradas")
except:
    print(sys.exc_info()[1])

listener_keyboard = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)

listener_mouse = mouse.Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll)

proc = Thread(target=procesamiento) #creacion del arbol en memoria
resp = Thread(target=respaldo) #creacion del respaldo

# inicio de los Hilos
proc.start()
resp.start()
listener_keyboard.start()
listener_mouse.start()
"""
#--------Interfaz grafica
seleccion=""
def seleccionar(evt):
    global seleccion
    seleccion=listbox1.get(listbox1.curselection())


def ejecutar(): # metodo para ejecutar la secuencia indicada
    d_acciones = {('1',): "1", ('2',): "2", ('3',): "3", ('4',): "4", ('5',): "5", ('6',): "6",
                  ('7',): "7", ('8',): "8", ('9',): "9", ('0',): "0", ('a',): "a", ('b',): "b",
                  ('c',): "c", ('d',): "d", ('e',): "e", ('f',): "f", ('g',): "g", ('h',): "h",
                  ('i',): "i", ('j',): "j", ('k',): "k", ('l',): "l", ('m',): "m", ('n',): "n",
                  ('ñ',): "ñ", ('o',): "o", ('p',): "p", ('q',): "q", ('r',): "r", ('s',): "s",
                  ('t',): "t", ('u',): "u", ('v',): "v", ('w',): "w", ('x',): "x", ('y',): "y",
                  ('z',): "z", ('A',): "A", ('B',): "B", ('C',): "C", ('D',): "D", ('E',): "E",
                  ('F',): "F", ('G',): "G", ('H',): "H", ('I',): "I", ('J',): "J", ('K',): "K",
                  ('L',): "L", ('M',): "M", ('N',): "N", ('Ñ',): "Ñ", ('O',): "O", ('P',): "P",
                  ('Q',): "Q", ('R',): "R", ('S',): "S", ('T',): "T", ('U',): "U", ('V',): "V",
                  ('W',): "W", ('X',): "X", ('Y',): "Y", ('Z',): "Z", ('.',): ".", (':',): ":",
                  (',',): ",", (';',): ";", ('-',): "-", ('_',): "_", ('<',): "<", ('>',): ">",
                  ('{',): "{", ('[',): "[", ('^',): "^", ('}',): "}", (']',): "]", ('`',): "`",
                  ('´',): "´", ('¨',): "¨", ('+',): "+", ('*',): "*", ('~',): "~", ('|',): "|",
                  ('°',): "°", ('¬',): "¬", ('!',): "!", ('"',): '"', ('#',): "#", ('$',): "$",
                  ('%',): "%", ('&',): "&", ('/',): "/", ('(',): "(", (')',): ")", ('=',): "=",
                  ("'",): "'", ('?',): "?", ('\\',): "\\", ('¿',): "¿", ('¡',): "¡", ('Key.ctrl_l',): keyboard.Key.ctrl_l,
                  ('Key.alt_l',): keyboard.Key.alt_l, ('Key.alt_r',): keyboard.Key.alt_r,
                  ('Key.ctrl_r',): keyboard.Key.ctrl_r, ('Key.left',): keyboard.Key.left,
                  ('Key.down',): keyboard.Key.down, ('Key.up',): keyboard.Key.up,
                  ('Key.right',): keyboard.Key.right, ('Key.shift_r',): keyboard.Key.shift_r,
                  ('Key.shift',): keyboard.Key.shift, ('Key.caps_lock',): keyboard.Key.caps_lock,
                  ('Key.enter',): keyboard.Key.enter, ('Key.tab',): keyboard.Key.tab,
                  ('Key.backspace',): keyboard.Key.backspace, ('Key.print_screen',): keyboard.Key.print_screen,
                  ('Key.delete',): keyboard.Key.delete, ('Key.insert',): keyboard.Key.insert,
                  ('Key.esc',): keyboard.Key.esc, ('Key.f1',): keyboard.Key.f1, ('Key.f2',): keyboard.Key.f2,
                  ('Key.f3',): keyboard.Key.f3,('Key.f4',): keyboard.Key.f4,('Key.f5',): keyboard.Key.f5,
                  ('Key.f6',): keyboard.Key.f6,('Key.f7',): keyboard.Key.f7,('Key.f8',): keyboard.Key.f8,
                  ('Key.f9',): keyboard.Key.f9,('Key.f10',): keyboard.Key.f10,('Key.f11',): keyboard.Key.f11,
                  ('Key.f12',): keyboard.Key.f12,('Key.num_lock',): keyboard.Key.num_lock,
                  ('Key.end',): keyboard.Key.end,('Key.home',): keyboard.Key.home,
                  ('Key.page_down',): keyboard.Key.page_down,('Key.page_up',): keyboard.Key.page_up,
                  ('Key.pause',): keyboard.Key.pause,('Key.space',): keyboard.Key.space,
                  ('Key.scroll_lock',): keyboard.Key.scroll_lock, ('Key.menu',): keyboard.Key.menu,
                  ('Key.cmd',): keyboard.Key.cmd, ('Key.alt_gr',): keyboard.Key.alt_gr,
                  ('Button.left',): mouse.Button.left, ('Button.right',): mouse.Button.right,
                  ('Button.middle',): mouse.Button.middle}
    #print("Total de acciones: ",len(d_acciones))
    k = keyboard.Controller()
    k.press(keyboard.Key.alt_l)
    k.press(keyboard.Key.tab)
    k.release(keyboard.Key.tab)
    k.release(keyboard.Key.alt_l)
    time.sleep(.5)
    for nodo in d_secuencias[seleccion]:
        espera=nodo.getTiempo()
        info = nodo.getInformacion()
        dispositivo = info[0]
        accion = info[1]
        disposicion = info[2:]
        time.sleep(espera)
        if dispositivo == "Keyboard":
            if accion == "Pressed":
                k.press(d_acciones[disposicion])
            else:
                k.release(d_acciones[disposicion])
        else:
            m = mouse.Controller()
            if accion == "Pressed":
                m.press(d_acciones[disposicion])
            if accion == "Released":
                m.release(d_acciones[disposicion])
            if accion == "Scrolled":
                if disposicion == "Down\n":
                    m.scroll(0)
                else:
                    m.scroll(1)
            if accion == "Moved":
                m.position = disposicion
    k.press(keyboard.Key.alt_l)
    k.press(keyboard.Key.tab)
    k.release(keyboard.Key.tab)
    k.release(keyboard.Key.alt_l)


master = Tk()
listbox1 = Listbox(master)
listbox1.get(ACTIVE)
listbox1.bind('<<ListboxSelect>>',seleccionar)
listbox1.pack()
for item in d_secuencias.keys():
    listbox1.insert(END, item)
boton=Button(master,text="Ejecutar Accion", command=ejecutar)
boton.pack()
master.title("Lista de Acciones")


resp = Thread(target=respaldo) #creacion del respaldo
resp.start()

#Carga de respaldo en disco
try:
    print("carga", "l_acciones")
    carga("l_acciones")
    print("Datos Cargados")
except:
    print(sys.exc_info()[1])

master.mainloop()
