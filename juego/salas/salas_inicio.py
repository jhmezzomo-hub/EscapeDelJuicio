import pygame, sys, os
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controlador.rutas import rutas_img
from controlador.cargar_fondos import cargar_fondo

# Inicializar Pygame
pygame.init()

# Pantalla fija
WIDTH, HEIGHT = 1100, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sala Jugable en el Piso Rojo")

# Cargar fondo
fondo = cargar_fondo(WIDTH, HEIGHT)

# Cargar personaje
path = rutas_img("michael-myers.png")
personaje = pygame.image.load(path)
personaje = pygame.transform.scale(personaje, (120, 200))
personaje_rect = personaje.get_rect(center=(WIDTH//2, HEIGHT - 150))

# Velocidad
velocidad = 5

# ---- CREAR MÁSCARA TRAPEZOIDAL ----
zona_jugable = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
zona_jugable.fill((0, 0, 0, 0))

arr = pygame.surfarray.array3d(fondo)

# Trapecio a mano (ajustado a tu imagen)
p1 = (200, 250)   # arriba izquierda
p2 = (900, 250)   # arriba derecha
p3 = (1050, 600)  # abajo derecha
p4 = (50, 600)    # abajo izquierda

puntos_trapecio = [p1, p2, p3, p4]

# Dibujar el polígono en la superficie
pygame.draw.polygon(zona_jugable, (255, 255, 255), puntos_trapecio)

# Crear máscara
mask = pygame.mask.from_surface(zona_jugable)

# Bucle principal
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Guardar posición original para revertir si sale de zona
    old_pos = personaje_rect.topleft

    if keys[pygame.K_w]:
        personaje_rect.y -= velocidad
    if keys[pygame.K_s]:
        personaje_rect.y += velocidad
    if keys[pygame.K_a]:
        personaje_rect.x -= velocidad
    if keys[pygame.K_d]:
        personaje_rect.x += velocidad
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

    # ---- Verificación dentro del bucle ----
    cx = personaje_rect.centerx
    cy = personaje_rect.bottom - 10

    if 0 <= cx < WIDTH and 0 <= cy < HEIGHT:
        if mask.get_at((cx, cy)) == 0:
            personaje_rect.topleft = old_pos
    else:
        personaje_rect.topleft = old_pos

    # Dibujar fondo
    screen.blit(fondo, (0, 0))

    # [Opcional] dibujar contorno del área jugable para depurar
    pygame.draw.polygon(screen, (0, 255, 0), puntos_trapecio, 2)

    # Dibujar personaje
    screen.blit(personaje, personaje_rect)

    pygame.display.flip()
    clock.tick(60)
