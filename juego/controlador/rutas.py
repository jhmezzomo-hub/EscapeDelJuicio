import os

def rutas_img(nombre_img, nombre_carpeta):
    path = os.path.dirname(__file__)
    path = os.path.abspath(os.path.join(path, "..","..","img", nombre_carpeta, nombre_img))
    return path  

def rutas_data(nombre_arch):
    path = os.path.dirname(__file__)
    path = os.path.join(path, "..","..","data", nombre_arch)
    return path

def rutas_juego(nombre_arch):
    path = os.path.dirname(__file__)
    path = os.path.join(path, nombre_arch)
    return path