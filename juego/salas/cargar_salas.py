import pygame, sys

from controlador.cargar_fondos import cargar_fondo
from limite_colisiones.colision_piso import colision_piso
from controlador.controles import manejar_mc
from juego.ui.inventory import Inventory

def cargar_sala(fondo, personaje_info, size):
    """Carga una sala con un fondo dado. 
    Más adelante podés expandirla con enemigos, puertas, etc."""
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Escape Del Juicio")

    # Fondo según el nombre
    fondo_1P = fondo
    fondo_2P = cargar_fondo("Fondo_sala1.png", "Fondos", size)

    # Inventario
    inv = Inventory(rows=5, cols=6, quickbar_slots=8, pos=(40, 40))
    inv.is_open = False

    # Hexágono igual que antes
    mask = colision_piso(size)

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
        manejar_mc(personaje_info[1], inv, mask, velocidad, maniquies=[])
        inv.update(dt)

        # Dibujos
        persoanje, personaje_rect = personaje_info
        screen.blit(fondo_1P, (0, 0))
        screen.blit(persoanje, personaje_rect)
        inv.draw(screen)
        pygame.display.flip()
