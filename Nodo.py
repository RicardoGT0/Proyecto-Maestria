# -*- coding: utf-8 -*-

class Nodo:
    def __init__(self, tiempo, informacion):
        self.__informacion = informacion
        self.__tiempo=tiempo
        self.__siguiente=[]
        self.__cuenta=0

    def cuenta(self):
        self.__cuenta+=1

    def siguiente_nodo(self,siguiente):
        self.__siguiente.append(siguiente)

    def getCuenta(self):
        return self.__cuenta

    def getInformacion(self):
        return self.__informacion

    def getTiempo(self):
        return self.__tiempo

    def setTiempo(self,tiempo):
        self.__tiempo=tiempo

    def getSiguiente_nodo(self):
        return self.__siguiente