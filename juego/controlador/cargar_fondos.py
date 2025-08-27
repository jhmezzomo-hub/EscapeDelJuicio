import pygame, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controlador.rutas import rutas_img

def cargar_fondo(WIDTH, HEIGHT):
    path = rutas_img("Fondo_Juego.png")
    fondo = pygame.image.load(path)
    fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))
    return fondo