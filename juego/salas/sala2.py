import pygame
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controlador.rutas import rutas_img
from controlador.cargar_fondos import cargar_fondo
from controlador.colisiones import crear_mascara
from controlador.cargar_personaje import cargar_personaje
from controlador.controles import manejar_mc
from juego.ui.inventory import Inventory

def iniciar_sala2():
    pygame.init()
    WIDTH, HEIGHT = 1100, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Escape Del Juicio - Sala 2")

    fuente = pygame.font.SysFont("Arial", 26)
    fondo = cargar_fondo("Fondo_sala1.png", "Fondos", (WIDTH, HEIGHT))
    personaje, personaje_rect = cargar_personaje("mc_0.png", "mc", WIDTH, HEIGHT)
    velocidad = 5

    # Máscara para límites (hexágono)
    puntos_hexagono = [
        (132, 411), (980, 411), (1100, 488),
        (1100, 600), (0, 600), (0, 491)
    ]
    mask = crear_mascara(puntos_hexagono, WIDTH, HEIGHT)

    # MANIQUÍES dentro del hexágono con espacio suficiente para pasar
    maniquies = []
    posiciones = [
        (900, 250),  # izquierda arriba
        (950, 370),  # izquierda media
        (700, 340),  # derecha media
        (100, 400),  # derecha arriba
        (150, 250),  # izquierda abajo
        (300, 300)   # derecha abajo
    ]
    imagenes = ["mm1.png", "mm2.png", "mm3.png", "mm4.png", "mm5.png", "mm6.png"]
    for img, pos in zip(imagenes, posiciones):
        maniquie_img, maniquie_rect = cargar_personaje(img, "Michael Myers", WIDTH, HEIGHT)
        maniquie_rect.topleft = pos
        maniquies.append((maniquie_img, maniquie_rect))

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

        manejar_mc(personaje_rect, velocidad, inv, mask)

        # DIBUJAR
        screen.blit(fondo, (0, 0))
        for img, rect in maniquies:
            screen.blit(img, rect)
            if personaje_rect.colliderect(rect):
                texto = fuente.render("¡Colisión con maniquí!", True, (255, 0, 0))
                screen.blit(texto, (WIDTH // 2 - texto.get_width() // 2, HEIGHT - 40))

        screen.blit(personaje, personaje_rect)
        inv.update(dt)
        inv.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    iniciar_sala2()
