
import time

class Listener:
    def tiempo(self, t_final):
        global lista
        global t_inicial
        t_total = round(t_final - t_inicial, 2)
        t_inicial = time.time()
        return t_total

    def on_move(self, x, y):
        global lista
        colocacion = ('{0},{1}'.format(x, y))
        lista.append((self.tiempo(time.time()), "Mouse", "Moved", colocacion))

    def on_click(self, x, y, button, pressed):
        global lista
        accion = "{0}".format('Pressed' if pressed else 'Released')
        lista.append((self.tiempo(time.time()), "Mouse", accion, str(button)))

    def on_scroll(self, x, y, dx, dy):
        global lista
        colocacion = ('{0}'.format('Down' if dy < 0 else 'Up'))
        lista.append((self.tiempo(time.time()), "Mouse", "Scrolled", colocacion))

    def on_press(self, key):
        global lista
        try:
            lista.append((self.tiempo(time.time()), "Keyboard", "Pressed", key.char))
        except AttributeError:
            lista.append((self.tiempo(time.time()), "Keyboard", "Pressed", str(key)))
        except TypeError:
            pass

    def on_release(self, key):
        global lista
        try:
            lista.append((self.tiempo(time.time()), "Keyboard", "Release", key.char))
        except AttributeError:
            lista.append((self.tiempo(time.time()), "Keyboard", "Release", str(key)))
        except TypeError:
            pass