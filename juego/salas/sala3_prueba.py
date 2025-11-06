import pygame
import sys
import os
import random
import math
import pygame.freetype

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from juego.controlador.cargar_fondos import cargar_fondo
from juego.controlador.verificar_colisiones import crear_mascara
from juego.controlador.cargar_personaje import cargar_personaje
from juego.controlador.controles import manejar_mc
from juego.ui.inventory import Inventory, Item
from info_pantalla.info_pantalla import info_pantalla, tamaño_pantallas
from juego.pantalla.pantalla_inicio import pantalla_de_inicio

# ------------------- SALA 2 -------------------
def iniciar_sala2():
    random.seed()

    size = tamaño_pantallas()
    screen = info_pantalla()
    fuente = pygame.font.SysFont("Arial", 26)
    personaje, personaje_rect = cargar_personaje("mc_0.png", "mc", size)
    velocidad = 5

    puntos_hexagono = [
        (132, 411), (980, 411), (1100, 488),
        (1100, 600), (0, 600), (0, 491)
    ]
    mask = crear_mascara(puntos_hexagono, *size)

    hitbox_rect = pygame.Rect(
        maniquie_rect.left + 20,
        maniquie_rect.bottom - 30 if pos[1] > 250 else maniquie_rect.top - 3,
        maniquie_rect.width - 40,
        30
    )

    profundidad = (maniquie_rect.top, maniquie_rect.bottom)

    inv = Inventory(rows=5, cols=6, quickbar_slots=8, pos=(40, 40))
    inv.is_open = False

    linterna_item = Item(type="linterna", count=1, max_stack=1, color=(255, 255, 150), image=None)
    inv.inventory_slots[0] = linterna_item

    clock = pygame.time.Clock()

    while True:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            inv.handle_event(event)

        teclas = pygame.key.get_pressed()
        if not inv.is_open and teclas[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

        manejar_mc(personaje_rect, inv, mask, velocidad, maniquies)

        inv.update(dt)
        inv.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    iniciar_sala2()
