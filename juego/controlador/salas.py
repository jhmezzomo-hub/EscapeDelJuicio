import pygame, sys, os

from controlador.cargar_fondos import cargar_fondo
from controlador.cargar_personaje import cargar_personaje
from controlador.colisiones import crear_mascara
from controlador.controles import manejar_mc
from juego.ui.inventory import Inventory

def cargar_sala(nombre_fondo, carpeta):
    """Carga una sala con un fondo dado. 
       Más adelante podés expandirla con enemigos, puertas, etc."""
    pygame.init()
    WIDTH, HEIGHT = 1100, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f"Sala: {nombre_fondo}")

    # Fondo según el nombre
    fondo = cargar_fondo(WIDTH, HEIGHT, nombre_fondo, carpeta)

    # Personaje
    personaje, personaje_rect = cargar_personaje("mc_0.png", "mc", WIDTH, HEIGHT)

    # Inventario
    inv = Inventory(rows=5, cols=6, quickbar_slots=8, pos=(40, 40))
    inv.is_open = False

    # Hexágono igual que antes
    puntos_hexagono = [
        (132, 411),
        (980, 411),
        (1100, 488),
        (1100, 600),
        (0, 600),
        (0, 491)
    ]
    mask = crear_mascara(puntos_hexagono, WIDTH, HEIGHT)

    velocidad = 5
    clock = pygame.time.Clock()

    while True:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            inv.handle_event(event)

            if not inv.is_open:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

        # Movimiento
        manejar_mc(personaje_rect, velocidad, inv, mask)
        inv.update(dt)

        # Dibujos
        screen.blit(fondo, (0, 0))
        screen.blit(personaje, personaje_rect)
        inv.draw(screen)
        pygame.display.flip()
