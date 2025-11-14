import pygame
from juego.controlador.verificar_colisiones import verificar_colision, verificar_colision_maniquies
from juego.controlador.inventario import crear_inventario
from juego.controlador.mensaje_paso_sala import devolver_pies_personaje

def teclas_movimiento(personaje_rect, velocidad, inv, mask, maniquies, last_direction="left", disable_movement=False):
    """Mueve el rect del personaje y devuelve (moving, direction).

    Cuando no hay tecla de movimiento, devuelve la `last_direction` sin
    cambiarla, de modo que el render pueda mantener la orientación.
    """
    # Inicializar para asegurar valores incluso si inv.is_open es True
    moving = False
    direction = last_direction

    if not inv.is_open and not disable_movement:
        old_pos = personaje_rect.topleft
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
        if verificar_colision(mask, devolver_pies_personaje(personaje_rect)) or verificar_colision_maniquies(maniquies, personaje_rect):
            personaje_rect.topleft = old_pos

    return moving, direction

