import time
from os import remove
import Arbol

class Archivo(Arbol):
    def carga(self, nombre_archivo):
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
                        Arbol.crear_rama(linea=linea, bandera=1)

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

    def respaldo(self):
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
                self.escribir_accion(["--", llave], "\l_secuencias")
                secuencia = d_secuencias[llave]
                print(d_secuencias)
                for accion in secuencia:
                    self.escribir_accion(accion.getInformacion(), "\l_secuencias")

            for secuencia in l_ignoradas:
                print(secuencia)
                self.escribir_accion(["--"], "\l_ignoradas")
                for accion in secuencia:
                    self.escribir_accion(accion.getInformacion(), "\l_ignoradas")
            time.sleep(30)

    def escribir_accion(self, accion, archivo):
        # Escribe tuplas o listas en el archivo especificado en un formato de valores separados por comas
        n_archivo = "C:\Capturador" + archivo + ".txt"
        archivo = open(n_archivo, "a")
        cadena = ""
        for elemento in accion:
            cadena += str(elemento) + ","
        archivo.write(cadena[:-1] + "\n")
        archivo.close()