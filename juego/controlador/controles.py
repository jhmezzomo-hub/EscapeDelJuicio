import pygame
from juego.controlador.verificar_colisiones import verificar_colision 

def teclas_movimiento(personaje_rect, velocidad, last_direction="left"):
    """Mueve el rect del personaje y devuelve (moving, direction).

    Cuando no hay tecla de movimiento, devuelve la `last_direction` sin
    cambiarla, de modo que el render pueda mantener la orientación.
    """
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
    return moving, direction

def manejar_mc(personaje_rect, inv, mask):
    # Movimiento del personaje: solo si el inventario NO está abierto
    old_pos = personaje_rect.topleft
    if not inv.is_open:
        # usar una velocidad por defecto (consistente con otras partes)
        # ignoramos la dirección devuelta aquí (este handler solo gestiona colisiones)
        teclas_movimiento(personaje_rect, 5)
        # ---- Verificación de colisión ----
        if not verificar_colision(mask, personaje_rect):
            personaje_rect.topleft = old_pos
