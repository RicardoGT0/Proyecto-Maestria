from pynput import mouse, keyboard
from threading import Thread
import time, sys

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
