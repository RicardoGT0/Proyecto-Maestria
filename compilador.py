import os
ruta = "C:\\Users\\pikac\\MEGA\\GitHub\\AI-Python\\Reportes\\Discapacitado"

lista_archivo = os.listdir(ruta)   # no especificar ruta para tomar el directorio actual
print(lista_archivo)

compilado=open(ruta+"\\compilado.txt",'a')

for archivo in lista_archivo:
    contenido=(open(ruta+"\\"+archivo, "r"))  # lectura del archivo
    for linea in contenido:
        compilado.write(linea)
    contenido.close()
compilado.close()





