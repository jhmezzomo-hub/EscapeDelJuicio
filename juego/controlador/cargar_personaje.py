import os, sys, pygame

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from juego.controlador.rutas import rutas_img

def cargar_personaje(nombre_img, personaje, size, tamaño):
    path = rutas_img(nombre_img, personaje)
    imagen = pygame.image.load(path)
    try:
        if pygame.display.get_surface() is not None:
            # Preferimos mantener el canal alpha si existe
            try:
                imagen = imagen.convert_alpha()
            except Exception:
                imagen = imagen.convert()
    except Exception:
        pass
    personaje = pygame.transform.scale(imagen, tamaño)
    personaje_rect = personaje.get_rect(center=(size[0]//2, size[1] - 150))
    return personaje, personaje_rect