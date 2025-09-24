import pygame
import sys
from juego.controlador import cargar_personaje


def iniciar_sala2():
    cargar_sala("Fondo_sala1.png", "Fondos")
    pygame.init()
    WIDTH, HEIGHT = 1100, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sala 2")

    personaje, personaje_rect = cargar_personaje("mc_0.png", "mc", WIDTH, HEIGHT)
    puerta_interaccion = pygame.Rect(770, 400, 120, 40)
    marron = (139, 69, 19)
    cuadrado_rect = pygame.Rect(400, 250, 100, 100)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((255, 255, 255))

        # Dibuja el personaje
        screen.blit(personaje, personaje_rect)

        # Dibuja la puerta
        pygame.draw.rect(screen, (255, 0, 0), puerta_interaccion, 2)

        # Dibuja el cuadrado marrón
        pygame.draw.rect(screen, marron, cuadrado_rect)

        pygame.display.flip()