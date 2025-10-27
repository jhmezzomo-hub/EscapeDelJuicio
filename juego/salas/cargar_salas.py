import pygame, sys

from juego.controlador.cargar_fondos import cargar_fondo
from juego.controlador.cargar_personaje import cargar_personaje
from limite_colisiones.colision_piso import colision_piso, devolver_puntos_hexagono
from juego.controlador.sprites_caminar import sprites_caminar
from juego.controlador.controles import teclas_movimiento
from info_pantalla.info_pantalla import tamaño_pantallas, info_pantalla
from juego.controlador.inventario import crear_inventario
from juego.controlador.cargar_config import get_config_sala
from juego.salas.salas_inicio import SalaInicio
from juego.salas.sala2 import Sala2
from juego.controlador.sprites_caminar import direction

def cargar_sala(nombre_sala, mask, maniquies=[]):
    """Carga una sala con un fondo dado."""

    size = tamaño_pantallas()
    screen = info_pantalla()
    fuente = pygame.font.SysFont("Arial", 26)
    config = get_config_sala(nombre_sala)

    pos_inicial = config["personaje"]["pos_inicial"],
    tamaño = config["personaje"]["tamaño"]

    fondo = cargar_fondo(config["fondo"], "Fondos")
    personaje, personaje_rect = cargar_personaje("mc_0.png", "mc", size, tamaño)

    # Create inventory with screen parameter
    inv = crear_inventario(screen)

    # Puerta
    puerta_interaccion_salida = config["puertas"]["salida"]
    try:
        puerta_interaccion_volver = config["puertas"]["volver"]
    except KeyError:
        puerta_interaccion_volver = None

    #pies_personjae
    pies_personaje = pygame.Rect(
        personaje_rect.centerx - 10,
        personaje_rect.bottom - 5,
        20, 5
    )

    puntos_hexagono = devolver_puntos_hexagono()
    mask = colision_piso(size)

    mostrar_contorno = False
    clock = pygame.time.Clock()
    velocidad = 5
    # Crear sala específica según el nombre
    if nombre_sala == "inicio":
        sala = SalaInicio(screen)
    elif nombre_sala == "sala2":
        sala = Sala2(screen)
    
    while True:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Dibujar fondo primero
        screen.blit(fondo, (0, 0))

        # Verificar colisiones antes de mover
        teclas_movimiento(direction, personaje_rect, velocidad, sala.inventario, mask, maniquies)

        # Renderizar sprites
        sprites_caminar(size, screen, sala.inventario, mask, maniquies, tamaño, personaje, personaje_rect)

        # Actualizar sala
        siguiente = sala.actualizar(personaje_rect, puerta_interaccion_salida)
        if siguiente:
            return siguiente

        pygame.display.flip()
