import pygame, sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from info_pantalla.info_pantalla import tamaño_pantallas

def ensombrecer(screen):
    sombra = pygame.Surface((screen.get_width(), screen.get_height()))  # Mismo tamaño que la pantalla
    sombra.set_alpha(100)  # Nivel de transparencia (0 = transparente, 255 = opaco)
    sombra.fill((0, 0, 0))  # Color negro

    # Dibujas la sombra encima del fondo
    screen.blit(sombra, (0, 0))