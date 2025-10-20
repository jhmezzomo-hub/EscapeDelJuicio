import pygame, sys

from juego.controlador.cargar_fondos import cargar_fondo
from juego.controlador.cargar_personaje import cargar_personaje
from limite_colisiones.colision_piso import colision_piso, devolver_puntos_hexagono
from juego.controlador.sprites_caminar import sprites_caminar
from info_pantalla.info_pantalla import tamaño_pantallas, info_pantalla
from juego.controlador.inventario import crear_inventario
from juego.controlador.cargar_config import get_config_sala

def cargar_sala(nombre_sala, maniquies=[]):
    """Carga una sala con un fondo dado.
    Más adelante podés expandirla con enemigos, puertas, etc."""

    size = tamaño_pantallas()
    screen = info_pantalla()
    fuente = pygame.font.SysFont("Arial", 26)
    config = get_config_sala(nombre_sala)

    pos_inicial = config["personaje"]["pos_inicial"],
    tamaño = config["personaje"]["tamaño"]

    fondo = cargar_fondo(config["fondo"], "Fondos")
    personaje, personaje_rect = cargar_personaje("mc_0.png", "mc", size, tamaño)

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
    inv = crear_inventario()

    clock = pygame.time.Clock()
    while True:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            inv.handle_event(event)

        if not inv.is_open:
            teclas = pygame.key.get_pressed()
            sprites_caminar(size, screen, inv, mask, maniquies, tamaño, personaje, personaje_rect)
            if teclas[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
            elif teclas[pygame.K_F1]:
                mostrar_contorno = not mostrar_contorno
            elif teclas[pygame.K_e]:
                if puerta_interaccion_salida:
                    if pies_personaje.colliderect(puerta_interaccion_salida):
                        return config["siguiente_sala"]
                if puerta_interaccion_volver:
                    if pies_personaje.colliderect(puerta_interaccion_volver) and puerta_interaccion_volver:
                        return config["sala_anterior"]

        # Empty list for maniquies since this room has none
        maniquies = maniquies if maniquies else []

        inv.update(dt)

        screen.blit(fondo, (0, 0))

        if mostrar_contorno:
            pygame.draw.polygon(screen, (0, 255, 0), puntos_hexagono, 2)
            pygame.draw.rect(screen, (0, 0, 255), personaje_rect, 1)
            pygame.draw.rect(screen, (0, 255, 255), pies_personaje, 2)
            pygame.draw.rect(screen, (255, 0, 0), puerta_interaccion_salida, 2)
            if puerta_interaccion_volver:
                pygame.draw.rect(screen, (255, 0, 0), puerta_interaccion_volver, 2)

        screen.blit(personaje, personaje_rect)

        if pies_personaje.colliderect(puerta_interaccion_salida):
            texto = fuente.render("Presiona E para pasar a la siguiente sala", True, (255, 255, 255))
            screen.blit(texto, (size[0] // 2 - texto.get_width() // 2, size[1] - 40))
        elif puerta_interaccion_volver and pies_personaje.colliderect(puerta_interaccion_volver):
            texto = fuente.render("Presiona E para volver a la sala anterior", True, (255, 255, 255))
            screen.blit(texto, (size[0] // 2 - texto.get_width() // 2, size[1] - 40))

        inv.draw(screen)
        pygame.display.flip()
        



