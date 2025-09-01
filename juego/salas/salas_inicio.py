import pygame, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controlador.rutas import rutas_img
from controlador.cargar_fondos import cargar_fondo
from controlador.colisiones import crear_mascara, verificar_colision

# Inicializar Pygame
pygame.init()

# Pantalla fija
WIDTH, HEIGHT = 1100, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sala Jugable con Hexágono en el Piso")

# Cargar fondo
fondo = cargar_fondo(WIDTH, HEIGHT)

# Cargar personaje
path = rutas_img("michael-myers.png")
personaje = pygame.image.load(path)
personaje = pygame.transform.scale(personaje, (120, 200))
personaje_rect = personaje.get_rect(center=(WIDTH//2, HEIGHT - 150))

# Velocidad
velocidad = 5

# ---- CREAR MÁSCARA HEXAGONAL (usando el controlador) ----
puntos_hexagono = [
    (132, 411),   # arriba izquierda
    (980, 411),   # arriba derecha
    (1100, 488),  # medio derecha
    (1100, 600),  # abajo derecha
    (0, 600),     # abajo izquierda
    (0, 491)      # medio izquierda
]

mask = crear_mascara(puntos_hexagono, WIDTH, HEIGHT)

# Flag para mostrar/ocultar el contorno
mostrar_contorno = False

# Bucle principal
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_F1:
                mostrar_contorno = not mostrar_contorno  # alternar debug

    keys = pygame.key.get_pressed()
    old_pos = personaje_rect.topleft

    # Movimiento
    if keys[pygame.K_w]:
        personaje_rect.y -= velocidad
    if keys[pygame.K_s]:
        personaje_rect.y += velocidad
    if keys[pygame.K_a]:
        personaje_rect.x -= velocidad
    if keys[pygame.K_d]:
        personaje_rect.x += velocidad

    # ---- Verificación de colisión (ahora con la función) ----
    if not verificar_colision(mask, personaje_rect):
        personaje_rect.topleft = old_pos

    # Dibujar fondo
    screen.blit(fondo, (0, 0))

    # Dibujar contorno del hexágono (solo si debug está activo)
    if mostrar_contorno:
        pygame.draw.polygon(screen, (0, 255, 0), puntos_hexagono, 2)

    # Dibujar personaje
    screen.blit(personaje, personaje_rect)

    pygame.display.flip()
    clock.tick(60)
