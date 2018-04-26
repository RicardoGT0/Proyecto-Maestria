import time

from Nodo import Nodo


class Arbol:

    def crear_rama(self,linea, bandera):
        global conteoMax, n_actual, d_nodos
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
                self.extraccion_secuencia()
        else:
            d_nodos[id_nodo] = n_nuevo
            n_actual.siguiente_nodo(n_nuevo)  # enlace de nodo nuevo
            n_actual = n_nuevo

    def extraccion_secuencia(self):
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


    def procesamiento(self):
        global lista
        while True:
            print(len(lista))
            for elemento in lista:
                self.crear_rama(elemento, 0)
                self.escribir_accion(elemento, "\l_acciones")
            lista = []
            time.sleep(5)
