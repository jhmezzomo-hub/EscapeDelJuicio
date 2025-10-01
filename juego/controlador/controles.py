import pygame
from .colisiones import verificar_colision, verificar_colision_maniquies

def manejar_mc(personaje_rect, velocidad, inv, mask, maniquies):
    keys = pygame.key.get_pressed()
    old_pos = personaje_rect.topleft

    if not inv.is_open:
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            personaje_rect.y -= velocidad
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            personaje_rect.y += velocidad
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            personaje_rect.x -= velocidad
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            personaje_rect.x += velocidad

        if not verificar_colision(mask, personaje_rect) or verificar_colision_maniquies(personaje_rect, maniquies):
            personaje_rect.topleft = old_pos
