import pygame
from juego.controlador.verificar_colisiones import verificar_colision, verificar_colision_maniquies

def teclas_movimiento(personaje_rect, velocidad, inv, mask, maniquies, last_direction="left"):
    """Mueve el rect del personaje y devuelve (moving, direction).

    Cuando no hay tecla de movimiento, devuelve la `last_direction` sin
    cambiarla, de modo que el render pueda mantener la orientación.
    """
    if not inv.is_open:
        old_pos = personaje_rect.topleft
        moving = False
        direction = last_direction
        keys = pygame.key.get_pressed()

        # Movimiento horizontal
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            personaje_rect.x -= velocidad
            moving = True
            direction = "left"
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            personaje_rect.x += velocidad
            moving = True
            direction = "right"

        # Movimiento vertical
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            personaje_rect.y -= velocidad
            moving = True
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            personaje_rect.y += velocidad
            moving = True

        # Comprobar colisiones: si hay colisión, revertimos al old_pos
        if verificar_colision(mask, personaje_rect) or verificar_colision_maniquies(maniquies, personaje_rect):
            personaje_rect.topleft = old_pos
    return moving, direction

        