import pygame, sys

from juego.limite_colisiones.colision_piso import devolver_puntos_hexagono
from controlador.cargar_fondos import cargar_fondo
from limite_colisiones.crear_mascara import crear_mascara
from controlador.controles import manejar_mc
from info_pantalla.info_pantalla import info_pantalla
from info_pantalla.mostrar_pantalla import mostrar_pantalla
from controlador.inventario import crear_inventario

def cargar_sala_1(fondo, personaje_info, size):
    """Carga una sala con un fondo dado. 
       Más adelante podés expandirla con enemigos, puertas, etc."""
    pygame.init()
    screen = info_pantalla()

    # Fondo según el nombre
    fondo_1P = fondo
    fondo_2P = cargar_fondo("Fondo_sala_2.png", "Fondos", size)

    # Inventario
    inv = crear_inventario()

    # Hexágono igual que antes
    puntos_hexagono = devolver_puntos_hexagono()
    mask = crear_mascara(puntos_hexagono, size)

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
        manejar_mc(personaje_info[1], velocidad, inv, mask)
        inv.update(dt)

        # Dibujos
        mostrar_pantalla(fondo_1P, personaje_info, screen, inv)