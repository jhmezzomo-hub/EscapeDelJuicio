import os, sys, pygame

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from juego.controlador.rutas import rutas_img

def cargar_img(nombre_img, carpeta, tamaño):
    path = rutas_img(nombre_img, carpeta)
    imagen = pygame.image.load(path).convert_alpha()
    imagen = pygame.transform.scale(imagen, tamaño)
    imagen_rect = imagen.get_rect(center= (tamaño[0]//2, tamaño[1]//2))
    return imagen, imagen_rect