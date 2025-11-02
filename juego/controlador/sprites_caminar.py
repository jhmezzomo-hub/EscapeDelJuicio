import pygame, sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from juego.controlador.cargar_personaje import cargar_personaje
from juego.controlador.controles import teclas_movimiento

def sprites_caminar(size, screen, inv, mask, maniquies, tamaño, personaje, personaje_rect):
    """Actualiza animación/movimiento del personaje y devuelve la superficie
    que debe pintarse para este frame (no dibuja directamente).

    Esto permite al llamador (p. ej. una sala) mezclar la superficie
    del personaje con otros objetos y ordenar por profundidad.
    """
    # Cargamos las superficies de las distintas animaciones (pueden seguir siendo
    # cargadas cada frame; idealmente se cachearían fuera de esta función)
    idle_left = cargar_personaje("mc_0.png", "mc", size, tamaño)[0]
    idle_right = pygame.transform.flip(idle_left, True, False)

    walk_left = [
        cargar_personaje("mc_1.png", "mc", size, tamaño)[0],
        cargar_personaje("mc_2.png", "mc", size, tamaño)[0],
    ]
    walk_right = [pygame.transform.flip(img, True, False) for img in walk_left]

    # ===== Variables del jugador =====
    velocidad = 5
    # Guardamos estado entre frames en atributos de la función
    walk_count = getattr(sprites_caminar, "walk_count", 0)
    direction = getattr(sprites_caminar, "direction", "left")

    # ===== Actualización por frame =====
    # `teclas_movimiento` modifica `personaje_rect` directamente y devuelve
    # si está moviendo y la nueva dirección sugerida.
    moving, new_direction = teclas_movimiento(personaje_rect, velocidad, inv, mask, maniquies, direction)

    # Actualizamos la dirección solo cuando hay movimiento horizontal
    if moving and new_direction in ("left", "right"):
        direction = new_direction

    # Selección de la superficie del personaje para este frame (no la dibujamos aquí)
    if moving:
        # ciclo de caminata
        frame = walk_count // 7 % len(walk_left)
        current_surf = walk_right[frame] if direction == "right" else walk_left[frame]
        walk_count += 1
        if walk_count >= 14:  # reiniciar ciclo
            walk_count = 0
    else:
        # idle
        walk_count = 0
        current_surf = idle_right if direction == "right" else idle_left

    # Guardamos el estado para el siguiente frame
    sprites_caminar.walk_count = walk_count
    sprites_caminar.direction = direction

    return current_surf
