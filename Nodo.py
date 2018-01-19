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

