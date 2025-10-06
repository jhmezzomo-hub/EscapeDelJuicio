import os, sys, pygame

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from juego.controlador.rutas import rutas_img

def cargar_personaje(nombre_img, personaje, size):
    path = rutas_img(nombre_img, personaje)
    personaje = pygame.image.load(path).convert_alpha()
    personaje = pygame.transform.scale(personaje, (120, 200))
    personaje_rect = personaje.get_rect(center=(size[0]//2, size[1] - 150))
    return personaje, personaje_rect