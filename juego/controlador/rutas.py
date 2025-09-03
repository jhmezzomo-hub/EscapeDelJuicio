import os, sys

def rutas_img(nombre_img, personaje=None):
    path = os.path.dirname(__file__)
    if personaje:
        path = os.path.join(path, "..","..","img", personaje, nombre_img)
    else:
        path = os.path.join(path, "..","..","img", nombre_img)
    path = os.path.abspath(path)
    return path

def rutas_data(nombre_arch):
    path = os.path.dirname(__file__)
    path = os.path.join(path, "..","..","data", nombre_arch)
    return path

def rutas_juego(nombre_arch):
    path = os.path.dirname(__file__)
    path = os.path.join(path, nombre_arch)
    return path