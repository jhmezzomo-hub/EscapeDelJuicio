import pygame, sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from juego.controlador.cargar_personaje import cargar_personaje
from juego.controlador.controles import teclas_movimiento

def sprites_caminar(size, screen, inv, mask, maniquies, tamaño, personaje, personaje_rect):
    """Maneja la animación y movimiento del personaje."""
    velocidad = 5
    direction = "right"
    frame = 0
    frame_rate = 10
    frame_count = 0
    
    # Get movement input
    moving, new_direction = teclas_movimiento(personaje_rect, velocidad, inv, mask, maniquies, direction)
    
    # Update animation frame
    if moving:
        frame_count += 1
        if frame_count >= frame_rate:
            frame = (frame + 1) % 4
            frame_count = 0
            
    # Draw character
    screen.blit(personaje, personaje_rect)
    
    # Draw inventory last
    inv.dibujar()
    
    return moving, new_direction
