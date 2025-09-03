import pygame

from juego.controlador.rutas import rutas_img

def cargar_fondo(WIDTH, HEIGHT):
    path = rutas_img("Fondo_inicial.png", "Fondos")
    fondo = pygame.image.load(path)
    fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))
    return fondo