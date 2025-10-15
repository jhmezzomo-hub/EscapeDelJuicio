import pygame, sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from juego.controlador.cargar_personaje import cargar_personaje
from juego.controlador.controles import teclas_movimiento

def sprites_caminar(size, screen, inv, mask,maniquies, tamaño):
# Cambiá estas rutas por las de tus imágenes
    personaje_rect = cargar_personaje("mc_0.png", "mc", size, tamaño)[1]
    idle_left = cargar_personaje("mc_0.png", "mc", size, tamaño)[0]
    idle_right = pygame.transform.flip(idle_left, True, False)

    walk_left = [
        cargar_personaje("mc_1.png", "mc", size, tamaño)[0],
        cargar_personaje("mc_2.png", "mc", size, tamaño)[0],
    ]
    walk_right = [pygame.transform.flip(img, True, False) for img in walk_left]

    # ===== Variables del jugador =====
    velocidad = 5
    walk_count = 0
    direction = "left"  # lado al que mira por defecto

    # ===== Loop principal =====
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(30)
        screen.fill((200, 200, 200))  # fondo gris

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Pasamos la dirección actual para que teclas_movimiento no la sobreescriba
        moving, new_direction = teclas_movimiento(personaje_rect, velocidad,  inv, mask, maniquies, direction,)
        # Solo actualizamos `direction` si hubo movimiento horizontal (left/right)
        # si moving es True y new_direction difiere, lo adoptamos. Si no, mantenemos
        # la dirección previa para que el personaje siga mirando hacia el último lado.
        if moving:
            direction = new_direction

        # Animación (usamos personaje_rect como posición fuente)
        if moving:
            if direction == "right":
                screen.blit(walk_right[walk_count // 7 % len(walk_right)], personaje_rect)
            else:
                screen.blit(walk_left[walk_count // 7 % len(walk_left)], personaje_rect)
            walk_count += 1
            if walk_count >= 14:  # 2 frames * 7 ticks
                walk_count = 0
        else:
            walk_count = 0
            if direction == "right":
                screen.blit(idle_right, personaje_rect)
            else:
                screen.blit(idle_left, personaje_rect)

        pygame.display.update()
