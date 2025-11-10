import pygame, sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from juego.controlador.cargar_personaje import cargar_personaje
from juego.controlador.controles import teclas_movimiento

def init_sprites(size, tamaño):
    """Inicializa y cachea las imágenes de sprites una sola vez"""
    if not hasattr(sprites_caminar, "sprites_cache"):
        idle_left = cargar_personaje("mc_0.png", "mc", size, tamaño)[0]
        idle_right = pygame.transform.flip(idle_left, True, False)

        walk_left = [
            cargar_personaje("mc_1.png", "mc", size, tamaño)[0],
            cargar_personaje("mc_2.png", "mc", size, tamaño)[0],
        ]
        walk_right = [pygame.transform.flip(img, True, False) for img in walk_left]

        sprites_caminar.sprites_cache = {
            "idle_left": idle_left,
            "idle_right": idle_right,
            "walk_left": walk_left,
            "walk_right": walk_right
        }

def sprites_caminar(size, screen, inv, mask, maniquies, tamaño, personaje, personaje_rect, disable_movement=False):
    """Actualiza animación/movimiento del personaje y devuelve la superficie
    que debe pintarse para este frame (no dibuja directamente).

    Esto permite al llamador (p. ej. una sala) mezclar la superficie
    del personaje con otros objetos y ordenar por profundidad.
    """
    # Inicializar caché de sprites si no existe
    init_sprites(size, tamaño)

    # Usar sprites cacheados
    sprites = sprites_caminar.sprites_cache

    # ===== Variables del jugador =====
    velocidad = 10
    # Guardamos estado entre frames en atributos de la función
    walk_count = getattr(sprites_caminar, "walk_count", 0)
    direction = getattr(sprites_caminar, "direction", "left")

    # ===== Actualización por frame =====
    # `teclas_movimiento` modifica `personaje_rect` directamente y devuelve
    # si está moviendo y la nueva dirección sugerida.
    moving, new_direction = teclas_movimiento(personaje_rect, velocidad, inv, mask, maniquies, direction, disable_movement)

    # Actualizamos la dirección solo cuando hay movimiento horizontal
    if moving and new_direction in ("left", "right"):
        direction = new_direction

    # Selección de la superficie del personaje para este frame (no la dibujamos aquí)
    if moving:
        # ciclo de caminata
        frame = walk_count // 7 % len(sprites["walk_left"])
        current_surf = sprites["walk_right"][frame] if direction == "right" else sprites["walk_left"][frame]
        walk_count += 1
        if walk_count >= 14:  # reiniciar ciclo
            walk_count = 0
    else:
        # idle
        walk_count = 0
        current_surf = sprites["idle_right"] if direction == "right" else sprites["idle_left"]

    # Guardamos el estado para el siguiente frame
    sprites_caminar.walk_count = walk_count
    sprites_caminar.direction = direction

    return current_surf
