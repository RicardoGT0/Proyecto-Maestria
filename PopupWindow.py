from tkinter import *

class popupWindow(object):
    def __init__(self,master,cadena):
        top=self.top=Toplevel(master)
        self.label1=Label(top,text="Que haces?(i)gnorar  (Escribe el nombre para guardar)")
        self.label1.pack()
        self.label2 = Label(top, text=str(cadena))
        self.label2.pack()
        self.entry1=Entry(top)
        self.entry1.pack()
        self.label3 = Label(top, text=" ")
        self.label3.pack()
        self.button1=Button(top,text='Guardar',command=self.cleanup)
        self.button1.pack()
        self.label4 = Label(top, text=" ")
        self.label4.pack()
        self.button2=Button(top,text="Ignorar", command=self.ignore)
        self.button2.pack()
        top.title("Captura de Accion")
    def cleanup(self):
        self.value=self.entry1.get()
        self.top.destroy()
    def ignore(self):
        self.value="ignorar secuencia"
        self.top.destroy()
