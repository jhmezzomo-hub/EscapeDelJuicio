import pygame
from juego.controlador.verificar_colisiones import verificar_colision, verificar_colision_maniquies

def teclas_movimiento(personaje_rect, velocidad, inv, mask, maniquies, direction):
    """Maneja el movimiento del personaje mediante el teclado."""
    keys = pygame.key.get_pressed()
    moving = False
    new_direction = direction
    
    # Remove the inventory open check since we don't use that anymore
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        personaje_rect.x -= velocidad
        moving = True
        new_direction = "left"
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        personaje_rect.x += velocidad
        moving = True
        new_direction = "right"
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        personaje_rect.y -= velocidad
        moving = True
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        personaje_rect.y += velocidad
        moving = True

    # Verificar colisiones
    verificar_colisiones(personaje_rect, mask, maniquies)
    
    return moving, new_direction

def verificar_colisiones(personaje_rect, mask, maniquies):
    """Verifica si el personaje colisiona con el mapa o con los maniquies."""
    if verificar_colision(mask, personaje_rect) or verificar_colision_maniquies(maniquies, personaje_rect):
        personaje_rect.topleft = personaje_rect.topleft

