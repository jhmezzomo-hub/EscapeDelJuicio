import pygame
from juego.controlador.verificar_colisiones import verificar_colision

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
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            personaje_rect.x -= velocidad
            moving = True
            direction = "left"
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            personaje_rect.x += velocidad
            moving = True
            direction = "right"
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            personaje_rect.y -= velocidad
            moving = True
            # No cambiamos la orientación horizontal al mover verticalmente
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            personaje_rect.y += velocidad
            moving = True
            # No cambiamos la orientación horizontal al mover verticalmente
        if not verificar_colision(mask, personaje_rect, maniquies):
            personaje_rect.topleft = old_pos
    return moving, direction

        