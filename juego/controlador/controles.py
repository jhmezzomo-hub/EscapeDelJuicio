import pygame
from .colisiones import verificar_colision 

def manejar_mc(personaje_rect, velocidad, inv, mask):
    """
    Maneja el movimiento del personaje principal usando WASD
    """
    keys = pygame.key.get_pressed()
    old_pos = personaje_rect.topleft
    if not inv.is_open:
        if keys[pygame.K_w]:
            personaje_rect.y -= velocidad
        if keys[pygame.K_s]:
            personaje_rect.y += velocidad
        if keys[pygame.K_a]:
            personaje_rect.x -= velocidad
        if keys[pygame.K_d]:
            personaje_rect.x += velocidad
        # ---- Verificación de colisión ----
        if not verificar_colision(mask, personaje_rect):
            personaje_rect.topleft = old_pos