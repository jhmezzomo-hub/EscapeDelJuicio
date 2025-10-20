import pygame

from juego.controlador.rutas import rutas_img

def cargar_fondo(nombre_img, carpeta):
    size = (1100, 600)
    try:
        path = rutas_img(nombre_img, carpeta)
        fondo = pygame.image.load(path).convert()
        fondo = pygame.transform.smoothscale(fondo, size)
        return fondo
    except pygame.error as e:
        print(f"No se pudo cargar el fondo: {path}")
        raise SystemExit(e)