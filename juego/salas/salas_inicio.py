import pygame, os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controlador.rutas import rutas_img
from controlador.cargar_fondos import cargar_fondo
from controlador.colisiones import crear_mascara
from controlador.cargar_personaje import cargar_personaje
from controlador.controles import manejar_mc
from juego.ui.inventory import Inventory

# Importamos la sala dos
from juego.salas.sala2 import iniciar_sala2

def bienvenida_textos(tiempo_actual, tiempo_inicio, fuente, screen, fondo, personaje, personaje_rect):
    mensajes = [
        "Bienvenidos al Escape del Juicio",
        "Este es un juego de vida o muerte en el que te enfrentarás a desafíos mortales",
        "Tendrás que derrotar enemigos, resolver acertijos y escapar con vida",
        "Podrás escapar?"
    ]
    for i, mensaje in enumerate(mensajes):
        if tiempo_actual - tiempo_inicio < (i + 1) * 2000:
            texto_bienvenida = fuente.render(mensaje, True, (255, 255, 255))
            screen.blit(fondo, (0, 0))
            screen.blit(personaje, personaje_rect)
            screen.blit(texto_bienvenida, (screen.get_width() // 2 - texto_bienvenida.get_width() // 2, 600 - 70))
            pygame.display.flip()
            return True
    return False

def iniciar_sala():
    pygame.init()

    WIDTH, HEIGHT = 1100, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Escape Del Juicio")

    fuente = pygame.font.SysFont("Arial", 26)
    fondo = cargar_fondo("Fondo_inicial.png", "Fondos", (WIDTH, HEIGHT))
    personaje, personaje_rect = cargar_personaje("mc_0.png", "mc", WIDTH, HEIGHT)

    # Puerta
    puerta_interaccion = pygame.Rect(770, 400, 70, 40)
    velocidad = 5

    # Máscara para límites de movimiento
    puntos_hexagono = [
        (132, 411), (980, 411), (1100, 488),
        (1100, 600), (0, 600), (0, 491)
    ]
    mask = crear_mascara(puntos_hexagono, WIDTH, HEIGHT)

    mostrar_contorno = False
    inv = Inventory(rows=5, cols=6, quickbar_slots=8, pos=(40, 40))
    inv.is_open = False

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
                    # PASAR A SALA 2
                    pygame.quit()
                    iniciar_sala2()
                    return

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
            screen.blit(texto, (WIDTH // 2 - texto.get_width() // 2, HEIGHT - 40))

        inv.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    iniciar_sala()
