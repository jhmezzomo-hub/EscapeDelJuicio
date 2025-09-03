from .rutas import rutas_img
import pygame

def cargar_personaje(personaje, WIDTH, HEIGHT):
    path = rutas_img(personaje)
    personaje = pygame.image.load(path).convert_alpha()
    personaje = pygame.transform.scale(personaje, (120, 200))
    personaje_rect = personaje.get_rect(center=(WIDTH//2, HEIGHT - 150))
    return personaje, personaje_rect