import pygame

def crear_mascara(puntos, width, height):
    """
    Crea una máscara a partir de un polígono (zona jugable).
    puntos: lista de tuplas con coordenadas [(x1, y1), (x2, y2), ...]
    width, height: dimensiones de la pantalla
    """
    superficie = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.polygon(superficie, (255, 255, 255), puntos)
    return pygame.mask.from_surface(superficie)