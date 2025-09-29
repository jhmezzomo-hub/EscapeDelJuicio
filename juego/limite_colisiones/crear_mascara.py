import pygame

def crear_mascara(puntos, size):
    """
    Crea una máscara a partir de un polígono (zona jugable).
    puntos: lista de tuplas con coordenadas [(x1, y1), (x2, y2), ...]
    size: dimensiones de la pantalla (width, height)
    """
    superficie = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.polygon(superficie, (255, 255, 255), puntos)
    return pygame.mask.from_surface(superficie)