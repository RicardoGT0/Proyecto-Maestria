# -*- coding: utf-8 -*-

class Nodo:
    def __init__(self, dispositivo, accion, tiempo, colocacion):
        self.__dispositivo=dispositivo
        self.__accion=accion
        self.__tiempo=tiempo
        self.__colocacion=colocacion
        self.__siguiente=[]
        self.__cuenta=0

    def cuenta(self):
        self.__cuenta+=1

    def siguiente_nodo(self,siguiente):
        self.__siguiente.append(siguiente)

    def getDispositivo(self):
        return self.__dispositivo

    def getAccion(self):
        return self.__accion

    def getTiempo(self):
        return self.__tiempo

    def getColocacion(self):
        return self.__colocacion

    def getCuenta(self):
        return self.__cuenta