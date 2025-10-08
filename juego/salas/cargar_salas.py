import pygame, sys

from juego.controlador.cargar_fondos import cargar_fondo
from juego.controlador.cargar_personaje import cargar_personaje
from limite_colisiones.colision_piso import colision_piso, devolver_puntos_hexagono
from juego.controlador.controles import manejar_mc
from juego.ui.inventory import Inventory
from juego.pantalla.mensaje_bienvenida import bienvenida_textos
from info_pantalla.info_pantalla import tamaño_pantallas
from juego.controlador.inventario import crear_inventario

def cargar_sala(config):
    """Carga una sala con un fondo dado. 
    Más adelante podés expandirla con enemigos, puertas, etc."""
    screen = config["screen"]
    pygame.display.set_caption(config["caption"])
    fuente = pygame.font.SysFont("Arial", 26)
    size = tamaño_pantallas()
    
    fondo = cargar_fondo(config["fondo"], "Fondos", size)
    personaje, personaje_rect = cargar_personaje("mc_0.png", "mc", size)

    # Puerta
    puerta_interaccion = config["puertas"]["salida"]
    velocidad = 5

    puntos_hexagono = devolver_puntos_hexagono()
    mask = colision_piso(size)

    mostrar_contorno = False
    inv = crear_inventario()

    # Inicializar variables para la bienvenida
    mostrar_bienvenida = True
    tiempo_inicio = pygame.time.get_ticks()

    clock = pygame.time.Clock()
    while True:
        dt = clock.tick(60) / 1000.0

        if mostrar_bienvenida:
            tiempo_actual = pygame.time.get_ticks()
            if not bienvenida_textos(tiempo_actual, tiempo_inicio, fuente, screen, fondo, personaje, personaje_rect):
                mostrar_bienvenida = False
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            inv.handle_event(event)

        if not inv.is_open:
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
            elif teclas[pygame.K_F1]:
                mostrar_contorno = not mostrar_contorno
            elif teclas[pygame.K_e]:
                pies_personaje = pygame.Rect(
                    personaje_rect.centerx - 10,
                    personaje_rect.bottom - 5,
                    20, 5
                )
                if pies_personaje.colliderect(puerta_interaccion):
                    return 'sala2'

        # Empty list for maniquies since this room has none
        maniquies = []
        manejar_mc(personaje_rect, velocidad, inv, mask, maniquies)
        inv.update(dt)

        screen.blit(fondo, (0, 0))

        if mostrar_contorno:
            pygame.draw.polygon(screen, (0, 255, 0), puntos_hexagono, 2)
            pygame.draw.rect(screen, (0, 0, 255), personaje_rect, 1)
            pies_personaje = pygame.Rect(
                personaje_rect.centerx - 10,
                personaje_rect.bottom - 5,
                20, 5
            )
            pygame.draw.rect(screen, (0, 255, 255), pies_personaje, 2)
            pygame.draw.rect(screen, (255, 0, 0), puerta_interaccion, 2)

        screen.blit(personaje, personaje_rect)

        pies_personaje = pygame.Rect(
            personaje_rect.centerx - 10,
            personaje_rect.bottom - 5,
            20, 5
        )
        if pies_personaje.colliderect(puerta_interaccion):
            texto = fuente.render("Presiona E para pasar a la siguiente sala", True, (255, 255, 255))
            screen.blit(texto, (size[0] // 2 - texto.get_width() // 2, size[1] - 40))

        inv.draw(screen)
        pygame.display.flip()

       

