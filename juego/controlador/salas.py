import pygame, sys
from juego.controlador.cargar_fondos import cargar_fondo
from juego.controlador.cargar_personaje import cargar_personaje
from juego.controlador.colisiones import crear_mascara
from juego.ui.inventory import Inventory
from juego.controlador.controles import manejar_mc

def cargar_sala_base(nombre_fondo, carpeta_fondo):
    """
    Carga los elementos básicos que comparten todas las salas
    
    Args:
        nombre_fondo (str): Nombre del archivo de fondo
        carpeta_fondo (str): Nombre de la carpeta donde está el fondo
    
    Returns:
        dict: Diccionario con todos los elementos base de la sala
    """
    # Configuración básica
    WIDTH, HEIGHT = 1100, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    # Cargar elementos comunes
    fondo = cargar_fondo(nombre_fondo, carpeta_fondo, (WIDTH, HEIGHT))
    personaje, personaje_rect = cargar_personaje("mc_0.png", "mc", WIDTH, HEIGHT)
    inv = Inventory(rows=5, cols=6, quickbar_slots=8, pos=(40, 40))
    inv.is_open = False
    
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

    elementos_base = {
        "screen": screen,
        "fondo": fondo,
        "personaje": personaje,
        "personaje_rect": personaje_rect,
        "inventario": inv,
        "mask": mask,
        "velocidad": velocidad,
        "clock": clock,
        "width": WIDTH,
        "height": HEIGHT,
        "puntos_hexagono": puntos_hexagono
    }

    return elementos_base

def actualizar_sala_base(elementos):
    """
    Actualiza y dibuja los elementos básicos de una sala
    
    Args:
        elementos (dict): Diccionario con los elementos base de la sala
    """
    dt = elementos["clock"].tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elementos["inventario"].handle_event(event)

        if not elementos["inventario"].is_open:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    # Movimiento si el inventario está cerrado
    if not elementos["inventario"].is_open:
        manejar_mc(elementos["personaje_rect"], elementos["velocidad"], 
                   elementos["inventario"], elementos["mask"])

    elementos["inventario"].update(dt)

    # Dibujos base
    elementos["screen"].blit(elementos["fondo"], (0, 0))
    elementos["screen"].blit(elementos["personaje"], elementos["personaje_rect"])
    elementos["inventario"].draw(elementos["screen"])

    return dt
