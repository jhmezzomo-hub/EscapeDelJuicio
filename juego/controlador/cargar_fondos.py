import pygame

from juego.controlador.rutas import rutas_img

def cargar_fondo(WIDTH, HEIGHT, nombre, carpeta):
    path = rutas_img(nombre, carpeta)
    fondo = pygame.image.load(path)
    fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))
    return fondo
