import pygame
from juego.limite_colisiones.crear_mascara import crear_mascara

def devolver_puntos_hexagono():
    puntos_hexagono = [
        (132, 411),   # arriba izquierda
        (980, 411),   # arriba derecha
        (1100, 488),  # medio derecha
        (1100, 600),  # abajo derecha
        (0, 600),     # abajo izquierda
        (0, 491)      # medio izquierda
    ]
    return puntos_hexagono

def verificar_colisiones(personaje_rect, mask):
    """Verifica las colisiones del personaje con el piso"""
    pies_personaje = pygame.Rect(
        personaje_rect.centerx - 10,
        personaje_rect.bottom - 5,
        20, 5
    )
    
    if not mask.get_at((pies_personaje.centerx, pies_personaje.bottom)):
        return True
    return False

def colision_piso(size):
    """Crea y devuelve la máscara de colisiones del piso"""
    # ---- CREAR MÁSCARA HEXAGONAL (usando el controlador) ----
    
    mask = crear_mascara(devolver_puntos_hexagono(), size)
    return mask