import pygame

def tamaño_pantallas():
    WIDTH, HEIGHT = 1100, 600
    size = (WIDTH, HEIGHT)
    return size

def info_pantalla():
    screen = pygame.display.set_mode(tamaño_pantallas())
    pygame.display.set_caption("Escape Del Juicio")
    return screen